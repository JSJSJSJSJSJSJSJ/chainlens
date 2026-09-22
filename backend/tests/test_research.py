import copy
import json
from datetime import date

import pytest
from chainlens.cli import app as cli
from chainlens.config import DEFAULT_SNAPSHOT
from chainlens.database import make_engine
from chainlens.errors import DomainError
from chainlens.importer import import_snapshot, load_snapshot
from chainlens.models import Company, Evidence, Relationship, RelationshipEvidence, Score
from chainlens.schemas import QueryFilters, Snapshot
from chainlens.scoring import calculate_score, independent_count
from chainlens.service import ResearchService
from conftest import evidence, relationship
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typer.testing import CliRunner


def test_import_is_idempotent_and_scores_persist(engine, snapshot_file):
    assert import_snapshot(engine, snapshot_file)["status"] == "unchanged"
    with Session(engine) as session:
        counts = {
            model.__tablename__: session.scalar(select(func.count()).select_from(model))
            for model in (Company, Evidence, Relationship, RelationshipEvidence, Score)
        }
    assert counts == {
        "companies": 4,
        "evidence": 3,
        "relationships": 6,
        "relationship_evidence": 6,
        "scores": 6,
    }


def test_import_rejects_changed_version_without_mutation(engine, snapshot_file, payload):
    payload["relationships"][0]["business_description"] = "Changed synthetic claim"
    snapshot_file.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(DomainError, match="同一数据集版本"):
        import_snapshot(engine, snapshot_file)
    with Session(engine) as session:
        assert session.get(Relationship, "supply").business_description == "Synthetic supply claim"


def test_import_new_version_and_restore_old(engine, snapshot_file, tmp_path, payload):
    payload["metadata"]["dataset_version"] = "synthetic-v2"
    payload["relationships"] = payload["relationships"][:1]
    new = tmp_path / "new.json"
    new.write_text(json.dumps(payload), encoding="utf-8")
    assert import_snapshot(engine, new)["status"] == "imported"
    with Session(engine) as session:
        assert ResearchService(session).company("focus")["summary"]["relationship_count"] == 1
    assert import_snapshot(engine, snapshot_file)["status"] == "imported"


@pytest.mark.parametrize(
    "mutation",
    [
        "checksum",
        "duplicate",
        "missing_parent",
        "parent_chain",
        "cycle",
        "missing_entity",
        "missing_evidence",
        "future_source",
        "reversed_time",
        "review",
        "peer_dimension",
        "confirmation",
    ],
)
def test_snapshot_rejects_invalid_semantics(payload, mutation):
    if mutation == "checksum":
        payload["evidence"][0]["excerpt"] += " altered"
    if mutation == "duplicate":
        payload["companies"].append(copy.deepcopy(payload["companies"][0]))
    if mutation == "missing_parent":
        payload["companies"][0]["parent_id"] = "missing"
    if mutation == "parent_chain":
        payload["companies"][0]["parent_id"] = "alpha"
        payload["companies"][1]["parent_id"] = "missing"
    if mutation == "cycle":
        payload["companies"][0]["parent_id"] = "alpha"
        payload["companies"][1]["parent_id"] = "focus"
    if mutation == "missing_entity":
        payload["relationships"][0]["source_company_id"] = "missing"
    if mutation == "missing_evidence":
        payload["relationships"][0]["evidence_links"][0]["evidence_id"] = "missing"
    if mutation == "future_source":
        payload["evidence"][0]["published_at"] = "2026-09-17"
    if mutation == "reversed_time":
        payload["relationships"][0]["valid_from"] = "2026-01-01"
    if mutation == "review":
        payload["relationships"][0]["human_review_status"] = "approved"
    if mutation == "peer_dimension":
        payload["relationships"][3]["comparison_dimension"] = None
    if mutation == "confirmation":
        payload["relationships"][0]["evidence_links"] = []
    with pytest.raises(ValidationError):
        Snapshot.model_validate(payload)


def test_five_roles_and_supplier_direction(client):
    distribution = client.get("/api/companies/focus").json()["summary"]["distribution"]
    assert all(distribution.values()) and distribution["supplier"] == 2
    alpha = client.get("/api/companies/alpha/relationships?relationship_type=customer").json()
    assert [item["id"] for item in alpha["items"]] == ["supply"]
    focus = client.get("/api/companies/focus/relationships?relationship_type=supplier").json()
    assert {item["id"] for item in focus["items"]} == {"supply", "unknown"}
    investor = client.get("/api/relationships/invest").json()
    assert investor["source_company_id"] == "focus" and investor["target_company_id"] == "gamma"


def test_filter_search_alias_sort_pagination_and_graph(client):
    endpoint = "/api/companies/focus"
    items = client.get(endpoint + "/relationships?q=alias-alpha&sort=company_asc").json()["items"]
    assert [item["id"] for item in items] == ["partner", "supply"]
    first = client.get(endpoint + "/relationships?page_size=2&page=1").json()
    second = client.get(endpoint + "/relationships?page_size=2&page=2").json()
    assert first["total"] == 6 and not (
        {i["id"] for i in first["items"]} & {i["id"] for i in second["items"]}
    )
    all_items = client.get(
        endpoint + "/relationships?min_confidence=80&fact_status=confirmed&sort=date_desc"
    ).json()
    graph = client.get(
        endpoint + "/graph?min_confidence=80&fact_status=confirmed&sort=date_desc"
    ).json()
    assert [x["id"] for x in graph["edges"]] == [x["id"] for x in all_items["items"]]
    assert graph["displayed"] == graph["total"] and not graph["truncated"]
    assert client.get("/api/companies?q=ALIAS-ALPHA").json()["total"] == 1
    assert client.get(endpoint + "/relationships?q=no-match").json()["items"] == []


@pytest.mark.parametrize(
    "url,status",
    [
        ("/api/companies/missing", 404),
        ("/api/relationships/missing", 404),
        ("/api/relationships/missing/evidence", 404),
        ("/unknown", 404),
        ("/api/companies?page=0", 422),
        ("/api/companies?page_size=101", 422),
        ("/api/companies/focus/relationships?min_confidence=-1", 422),
        ("/api/companies/focus/relationships?min_confidence=101", 422),
        ("/api/companies/focus/relationships?relationship_type=bad", 422),
        ("/api/companies/focus/relationships?fact_status=bad", 422),
        ("/api/companies/focus/relationships?sort=bad", 422),
        ("/api/companies/focus/relationships?known_at=invalid", 422),
        ("/api/companies/focus/relationships?known_at=2026-09-17", 422),
        ("/api/companies/focus/graph?valid_at=2026-09-17", 422),
    ],
)
def test_errors_are_consistent(client, url, status):
    response = client.get(url)
    assert response.status_code == status
    assert set(response.json()["error"]) == {"code", "message", "details"}


def test_known_at_boundary_and_unknown_publication(client):
    url = "/api/companies/focus/relationships"
    assert client.get(url + "?known_at=2023-12-31").json()["total"] == 0
    at = client.get(url + "?known_at=2024-01-01").json()
    assert {item["id"] for item in at["items"]} == {"supply", "invest"}
    assert client.get("/api/relationships/customer?known_at=2024-01-01").status_code == 404
    assert client.get(url + "?known_at=2026-09-16&include_unknown_time=true").json()["total"] == 5
    assert client.get("/api/relationships/unknown/evidence?known_at=2026-09-16").status_code == 404


def test_valid_at_closed_open_and_unknown_boundaries(client):
    url = "/api/companies/focus/relationships?valid_at="
    assert {i["id"] for i in client.get(url + "2025-01-01").json()["items"]} == {"supply", "invest"}
    assert client.get(url + "2025-01-02").json()["total"] == 0
    at_cutoff = client.get(url + "2026-09-16").json()
    assert [i["id"] for i in at_cutoff["items"]] == ["customer"]
    unknown = client.get(url + "2026-09-16&include_unknown_time=true").json()["items"]
    assert {i["id"] for i in unknown} == {"customer", "unknown", "peer"}
    assert all("无法确证" in i["uncertainty"] for i in unknown if i["id"] != "customer")


def test_known_at_recalculates_without_later_or_conflicting_evidence(engine, payload, tmp_path):
    payload["metadata"]["dataset_version"] = "synthetic-conflict"
    payload["relationships"][0]["evidence_links"].append(
        {"evidence_id": "later", "stance": "contradicts", "directness": "direct"}
    )
    path = tmp_path / "conflict.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    import_snapshot(engine, path)
    with Session(engine) as session:
        svc = ResearchService(session)
        all_evidence = svc.relationship("supply")
        earlier = svc.relationship("supply", date(2024, 1, 1))
        assert earlier["score"]["total"] == all_evidence["score"]["total"] + 30
        assert earlier["evidence_count"] == 1 and all_evidence["evidence_count"] == 2


def test_scoring_determinism_duplicates_conflicts_caps_and_history(payload):
    rel = payload["relationships"][0]
    ev = dict(payload["evidence"][0], stance="supports", directness="direct")
    cutoff = date(2026, 9, 16)
    timestamp = "2026-09-16T00:00:00Z"
    score = calculate_score(rel, [ev], cutoff, timestamp)
    assert score == calculate_score(rel, [ev], cutoff, timestamp)
    assert score["total"] == sum(item["points"] for item in score["components"])
    assert all(item["reason"] for item in score["components"])
    duplicate = dict(ev, id="reprint", source_url="https://example.org/reprint")
    assert calculate_score(rel, [ev, duplicate], cutoff, timestamp) == score
    assert independent_count([ev, dict(ev, independence_key="fake-new-origin")]) == 1
    conflict = dict(evidence("conflict"), stance="contradicts", directness="direct")
    assert calculate_score(rel, [ev, conflict], cutoff, timestamp)["total"] == score["total"] - 30
    assert score["current_validity"] == "historical_only"
    assert (
        calculate_score(dict(rel, fact_status="inferred"), [ev], cutoff, timestamp)["total"] <= 69
    )
    assert calculate_score(dict(rel, fact_status="unknown"), [ev], cutoff, timestamp)["total"] <= 39
    assert calculate_score(dict(rel, quantitative_context="$1"), [ev], cutoff, timestamp) == score
    recent = dict(ev, published_at="2026-09-01")
    assert calculate_score(rel, [recent], cutoff, timestamp)["total"] == score["total"]
    assert (
        calculate_score(
            dict(rel, temporal_status="current", valid_to=None), [recent], cutoff, timestamp
        )["total"]
        > calculate_score(
            dict(rel, temporal_status="current", valid_to=None), [ev], cutoff, timestamp
        )["total"]
    )
    assert (
        calculate_score(rel, [dict(ev, published_at=None)], cutoff, timestamp)["total"]
        < score["total"]
    )


def test_api_and_cli_share_exact_json(client, engine, monkeypatch):
    monkeypatch.setenv("CHAINLENS_DATABASE_URL", str(engine.url))
    runner = CliRunner()
    for args, endpoint in [
        (["companies"], "/api/companies"),
        (["company", "focus"], "/api/companies/focus"),
        (
            ["relationships", "focus", "--relationship-type", "supplier"],
            "/api/companies/focus/relationships?relationship_type=supplier",
        ),
        (["graph", "focus"], "/api/companies/focus/graph"),
        (["evidence", "supply"], "/api/relationships/supply/evidence"),
    ]:
        result = runner.invoke(cli, args + ["--json"])
        assert result.exit_code == 0, result.output
        assert json.loads(result.output) == client.get(endpoint).json()
    invalid = runner.invoke(cli, ["relationships", "focus", "--page-size", "101", "--json"])
    assert invalid.exit_code == 1 and json.loads(invalid.output)["error"]["code"] == "INVALID_INPUT"


def test_graph_explicit_cap(engine, payload, tmp_path):
    payload["metadata"]["dataset_version"] = "synthetic-large"
    payload["relationships"] = [
        relationship(f"partner-{index:03}", "focus", "alpha", "partner") for index in range(105)
    ]
    path = tmp_path / "large.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    import_snapshot(engine, path)
    with Session(engine) as session:
        graph = ResearchService(session).graph("focus", QueryFilters())
    assert graph["total"] == 105 and graph["displayed"] == 100 and graph["truncated"]
    assert len(graph["nodes"]) == 2


def test_real_snapshot_integrity_and_five_role_coverage(tmp_path):
    # Real data test checks structure, never substitutes synthetic claims for research.
    snapshot, _ = load_snapshot(DEFAULT_SNAPSHOT)
    assert len(snapshot.companies) == 14 and len(snapshot.relationships) == 22
    assert all(item.human_review_status == "pending" for item in snapshot.relationships)
    engine = make_engine(f"sqlite:///{tmp_path / 'real.sqlite3'}")
    import_snapshot(engine, DEFAULT_SNAPSHOT)
    with Session(engine) as session:
        summary = ResearchService(session).company("nvidia")["summary"]
        assert summary["distribution"] == {
            "supplier": 5,
            "customer": 1,
            "partner": 9,
            "investor_or_investee": 2,
            "peer": 5,
        }
    engine.dispose()


def test_known_at_does_not_present_later_claim_as_earlier_fact(engine, payload, tmp_path):
    payload["metadata"]["dataset_version"] = "synthetic-promoted"
    links = payload["relationships"][0]["evidence_links"]
    links[0]["directness"] = "indirect"
    links.append({"evidence_id": "later", "stance": "supports", "directness": "direct"})
    path = tmp_path / "promoted.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    import_snapshot(engine, path)
    with Session(engine) as session:
        svc = ResearchService(session)
        earlier = svc.relationship("supply", date(2024, 1, 1))
        assert earlier["fact_status"] == "inferred"
        assert "候选关系" in earlier["business_description"]
        assert earlier["score"]["total"] <= 69
        assert svc.relationship("supply")["fact_status"] == "confirmed"
