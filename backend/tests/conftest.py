"""Entirely synthetic fixtures; no test record belongs to the research dataset."""

import hashlib
import json

import pytest
from app.db.session import make_engine
from app.main import create_app
from app.services.import_service import import_snapshot
from fastapi.testclient import TestClient


def company(identifier):
    return {
        "id": identifier,
        "legal_name": f"Synthetic {identifier.title()} Inc.",
        "display_name": identifier.title(),
        "aliases": [f"alias-{identifier}"],
        "ticker": identifier.upper(),
        "exchange": "SYNTHETIC",
        "listing_status": "listed",
        "parent_id": None,
        "identity_notes": "TEST ONLY",
    }


def evidence(identifier, published="2024-01-01", origin=None):
    excerpt = f"Synthetic claim {identifier}, not research evidence."
    return {
        "id": identifier,
        "title": f"Synthetic {identifier}",
        "source_url": f"https://example.org/{identifier}",
        "publisher": "Synthetic Publisher",
        "published_at": published,
        "retrieved_at": "2026-09-16T00:00:00Z",
        "evidence_locator": "Synthetic paragraph",
        "excerpt": excerpt,
        "interpretation": "TEST ONLY",
        "source_type": "regulatory",
        "independence_key": origin or identifier,
        "content_sha256": hashlib.sha256(excerpt.encode()).hexdigest(),
        "access_restrictions": "Synthetic",
        "redistribution_notes": "Synthetic",
    }


def relationship(identifier, source, target, kind, ev="early", **overrides):
    item = {
        "id": identifier,
        "source_company_id": source,
        "target_company_id": target,
        "relationship_type": kind,
        "business_description": f"Synthetic {identifier} claim",
        "fact_status": "confirmed",
        "valid_from": "2024-01-01",
        "valid_to": "2025-01-01",
        "temporal_status": "historical",
        "continuity_note": "TEST ONLY",
        "uncertainty": "Synthetic limitation",
        "human_review_status": "pending",
        "entity_resolution": "exact",
        "comparison_dimension": "Synthetic GPU comparison" if kind == "peer" else None,
        "quantitative_context": None,
        "evidence_links": [{"evidence_id": ev, "stance": "supports", "directness": "direct"}],
    }
    item.update(overrides)
    return item


@pytest.fixture
def payload():
    return {
        "metadata": {
            "dataset_version": "synthetic-v1",
            "research_cutoff": "2026-09-16",
            "score_version": "1.0.0",
            "created_at": "2026-09-16T00:00:00Z",
            "description": "SYNTHETIC TEST DATA, NOT RESEARCH",
            "gaps": ["TEST ONLY"],
        },
        "companies": [company(value) for value in ("focus", "alpha", "beta", "gamma")],
        "evidence": [evidence("early"), evidence("later", "2025-03-01"), evidence("undated", None)],
        "relationships": [
            relationship("supply", "alpha", "focus", "supplier"),
            relationship(
                "customer",
                "focus",
                "beta",
                "supplier",
                "later",
                valid_from="2025-03-01",
                valid_to=None,
                temporal_status="current",
            ),
            relationship(
                "partner",
                "focus",
                "alpha",
                "partner",
                "later",
                valid_from="2025-03-01",
                valid_to="2025-03-01",
            ),
            relationship(
                "peer",
                "focus",
                "gamma",
                "peer",
                "later",
                valid_from=None,
                valid_to=None,
                temporal_status="unknown",
            ),
            relationship("invest", "focus", "gamma", "investor_or_investee"),
            relationship(
                "unknown",
                "beta",
                "focus",
                "supplier",
                "undated",
                valid_from=None,
                valid_to=None,
                temporal_status="unknown",
                fact_status="unknown",
            ),
        ],
    }


@pytest.fixture
def snapshot_file(tmp_path, payload):
    path = tmp_path / "synthetic.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


@pytest.fixture
def engine(tmp_path, snapshot_file):
    engine = make_engine(f"sqlite:///{tmp_path / 'synthetic.sqlite3'}")
    import_snapshot(engine, snapshot_file)
    yield engine
    engine.dispose()


@pytest.fixture
def client(engine):
    with TestClient(create_app(engine=engine, auto_import=False)) as client:
        yield client
