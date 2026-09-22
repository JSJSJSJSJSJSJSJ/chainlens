"""CLI and HTTP share ResearchService, schemas, scoring, and offline import."""

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from .config import snapshot_path
from .database import make_engine
from .errors import DomainError
from .importer import ensure_dataset, import_snapshot
from .schemas import QueryFilters
from .service import ResearchService

app = typer.Typer(no_args_is_help=True, help="ChainLens 链鉴：固定快照的离线研究查询。")
JsonFlag = Annotated[bool, typer.Option("--json", help="输出与 HTTP API 相同的数据结构")]


def output(data, as_json):
    if as_json:
        typer.echo(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        return
    rows = data.get("items") if isinstance(data, dict) else None
    if rows and isinstance(rows[0], dict) and "display_name" in rows[0]:
        table = Table("ID", "公司", "证券", "交易所")
        for row in rows:
            table.add_row(row["id"], row["display_name"], row["ticker"], row["exchange"])
        Console().print(table)
        typer.echo(f"共 {data['total']} 条；第 {data['page']} 页")
    elif rows and isinstance(rows[0], dict) and "queried_role" in rows[0]:
        table = Table("ID", "关联公司", "角色", "状态", "置信度", "证据")
        for row in rows:
            table.add_row(
                row["id"],
                row["related_company"]["display_name"],
                row["queried_role"],
                row["fact_status"],
                str(row["score"]["total"]),
                str(row["evidence_count"]),
            )
        Console().print(table)
        typer.echo(f"共 {data['total']} 条；第 {data['page']} 页")
    else:
        Console().print_json(json.dumps(data, ensure_ascii=False, default=str))


@contextmanager
def query_service(as_json: bool):
    engine = None
    try:
        engine = make_engine()
        ensure_dataset(engine, snapshot_path())
        with Session(engine) as session:
            yield ResearchService(session)
    except DomainError as exc:
        output(exc.payload(), as_json)
        raise typer.Exit(1) from exc
    except ValidationError as exc:
        error = DomainError(
            "INVALID_INPUT",
            "查询参数格式或范围不正确",
            details=exc.errors(include_context=False, include_input=False),
        )
        output(error.payload(), as_json)
        raise typer.Exit(1) from exc
    finally:
        if engine:
            engine.dispose()


@app.command("import-snapshot")
def import_command(
    path: Annotated[Path | None, typer.Option("--path", help="快照JSON路径")] = None,
    as_json: JsonFlag = False,
):
    engine = make_engine()
    try:
        output(import_snapshot(engine, path or snapshot_path()), as_json)
    except DomainError as exc:
        output(exc.payload(), as_json)
        raise typer.Exit(1) from exc
    finally:
        engine.dispose()


@app.command()
def health(as_json: JsonFlag = False):
    with query_service(as_json) as service:
        output(service.health(), as_json)


@app.command()
def companies(q: str | None = None, page: int = 1, page_size: int = 20, as_json: JsonFlag = False):
    with query_service(as_json) as service:
        output(service.companies(q, page, page_size), as_json)


@app.command()
def company(company_id: str, as_json: JsonFlag = False):
    with query_service(as_json) as service:
        output(service.company(company_id), as_json)


def filters_from(
    q,
    relationship_type,
    min_confidence,
    fact_status,
    known_at,
    valid_at,
    include_unknown_time,
    page,
    page_size,
    sort,
):
    return QueryFilters(
        q=q,
        relationship_type=relationship_type,
        min_confidence=min_confidence,
        fact_status=fact_status,
        known_at=known_at,
        valid_at=valid_at,
        include_unknown_time=include_unknown_time,
        page=page,
        page_size=page_size,
        sort=sort,
    )


@app.command()
def relationships(
    company_id: str,
    q: str | None = None,
    relationship_type: str | None = None,
    min_confidence: int = 0,
    fact_status: str | None = None,
    known_at: str | None = None,
    valid_at: str | None = None,
    include_unknown_time: bool = False,
    page: int = 1,
    page_size: int = 20,
    sort: str = "confidence_desc",
    as_json: JsonFlag = False,
):
    with query_service(as_json) as service:
        filters = filters_from(
            q,
            relationship_type,
            min_confidence,
            fact_status,
            known_at,
            valid_at,
            include_unknown_time,
            page,
            page_size,
            sort,
        )
        output(service.relationships(company_id, filters), as_json)


@app.command()
def graph(
    company_id: str,
    q: str | None = None,
    relationship_type: str | None = None,
    min_confidence: int = 0,
    fact_status: str | None = None,
    known_at: str | None = None,
    valid_at: str | None = None,
    include_unknown_time: bool = False,
    sort: str = "confidence_desc",
    as_json: JsonFlag = False,
):
    with query_service(as_json) as service:
        filters = filters_from(
            q,
            relationship_type,
            min_confidence,
            fact_status,
            known_at,
            valid_at,
            include_unknown_time,
            1,
            100,
            sort,
        )
        output(service.graph(company_id, filters), as_json)


@app.command()
def relationship(relationship_id: str, known_at: str | None = None, as_json: JsonFlag = False):
    with query_service(as_json) as service:
        known = QueryFilters(known_at=known_at).known_at
        output(service.relationship(relationship_id, known), as_json)


@app.command()
def evidence(relationship_id: str, known_at: str | None = None, as_json: JsonFlag = False):
    with query_service(as_json) as service:
        known = QueryFilters(known_at=known_at).known_at
        output(service.evidence(relationship_id, known), as_json)


if __name__ == "__main__":
    app()
