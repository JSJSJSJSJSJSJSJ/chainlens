"""Offline, validated, atomic replacement of the active research dataset."""

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy import delete, update
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.core.errors import DomainError
from app.db.crud import get_active_dataset
from app.models import Company, Dataset, Evidence, Relationship, RelationshipEvidence, Score
from app.schemas import Snapshot
from app.services.scoring import calculate_score


def load_snapshot(path: Path) -> tuple[Snapshot, str]:
    try:
        raw = path.read_bytes()
        snapshot = Snapshot.model_validate_json(raw)
    except OSError as exc:
        raise DomainError("SNAPSHOT_UNAVAILABLE", f"无法读取快照：{path}") from exc
    except ValidationError as exc:
        raise DomainError(
            "INVALID_SNAPSHOT",
            "快照校验失败，未修改数据库",
            details=exc.errors(include_context=False, include_input=False),
        ) from exc
    return snapshot, hashlib.sha256(raw).hexdigest()


def import_snapshot(engine: Engine, path: Path) -> dict:
    snapshot, digest = load_snapshot(path)
    version = snapshot.metadata.dataset_version
    now = datetime.now(UTC)
    summary = {
        "dataset_version": version,
        "content_sha256": digest,
        "companies": len(snapshot.companies),
        "relationships": len(snapshot.relationships),
        "evidence": len(snapshot.evidence),
    }
    # Acquire SQLite's writer reservation before reading: concurrent startup/import is serialized.
    with engine.connect() as connection:
        if engine.dialect.name == "sqlite":
            connection.exec_driver_sql("BEGIN IMMEDIATE")
        with Session(bind=connection, join_transaction_mode="control_fully") as session:
            try:
                previous = session.get(Dataset, version)
                if previous and previous.content_sha256 != digest:
                    raise DomainError(
                        "DATASET_VERSION_CONFLICT", "同一数据集版本内容改变；请使用新版本号"
                    )
                if previous and previous.active:
                    session.commit()
                    return dict(summary, status="unchanged")
                for model in (RelationshipEvidence, Score, Relationship, Evidence):
                    session.execute(delete(model))
                # Null parent links first, including links between rows being replaced.
                session.execute(update(Company).values(parent_id=None))
                session.execute(delete(Company))
                session.execute(update(Dataset).values(active=False))
                for item in snapshot.companies:
                    session.add(Company(**item.model_dump(exclude={"parent_id"}), parent_id=None))
                session.flush()
                for item in snapshot.companies:
                    if item.parent_id:
                        session.get(Company, item.id).parent_id = item.parent_id
                for item in snapshot.evidence:
                    data = item.model_dump()
                    data["source_url"] = str(item.source_url)
                    session.add(Evidence(**data))
                session.flush()
                evidence_map = {item.id: item.model_dump(mode="json") for item in snapshot.evidence}
                for item in snapshot.relationships:
                    relation = Relationship(**item.model_dump(exclude={"evidence_links"}))
                    relation.evidence_links = [
                        RelationshipEvidence(**link.model_dump()) for link in item.evidence_links
                    ]
                    linked = [
                        dict(
                            evidence_map[link.evidence_id],
                            stance=link.stance,
                            directness=link.directness,
                        )
                        for link in item.evidence_links
                    ]
                    score = calculate_score(
                        item.model_dump(mode="json"), linked, snapshot.metadata.research_cutoff, now
                    )
                    score["calculated_at"] = now
                    relation.score = Score(**score)
                    session.add(relation)
                if previous:
                    previous.active = True
                    previous.imported_at = now
                else:
                    session.add(
                        Dataset(
                            version=version,
                            content_sha256=digest,
                            active=True,
                            metadata_json=snapshot.metadata.model_dump(mode="json"),
                            imported_at=now,
                        )
                    )
                session.commit()
            except Exception:
                session.rollback()
                raise
    return dict(summary, status="imported")


def ensure_dataset(engine: Engine, path: Path):
    with Session(engine) as session:
        active = get_active_dataset(session)
    if active is None:
        import_snapshot(engine, path)
