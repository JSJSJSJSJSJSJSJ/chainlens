"""One query service used by HTTP and CLI. Small curated datasets favor explicit rules."""

from datetime import UTC, date, datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .errors import DomainError
from .models import Company, Dataset, Relationship
from .schemas import QueryFilters
from .scoring import calculate_score, independent_count


def serialize(model) -> dict:
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.key)
        if isinstance(value, datetime):
            value = value.replace(tzinfo=UTC) if value.tzinfo is None else value
            value = value.isoformat()
        elif isinstance(value, date):
            value = value.isoformat()
        result[column.key] = value
    return result


def queried_role(relationship, company_id: str | None) -> str:
    if (
        relationship.relationship_type == "supplier"
        and company_id == relationship.source_company_id
    ):
        return "customer"
    return relationship.relationship_type


def matches_valid_at(relationship, at: date, include_unknown: bool, cutoff: date) -> bool:
    # A known exclusion always wins, even when the other boundary is unknown.
    if relationship.valid_from and relationship.valid_from > at:
        return False
    if relationship.valid_to and relationship.valid_to < at:
        return False
    start_known = relationship.valid_from is not None
    end_known = relationship.valid_to is not None or (
        relationship.temporal_status == "current" and at <= cutoff
    )
    return (start_known and end_known) or include_unknown


class ResearchService:
    def __init__(self, session: Session):
        self.session = session
        dataset = session.scalar(select(Dataset).where(Dataset.active.is_(True)))
        if dataset is None:
            raise DomainError("DATASET_UNAVAILABLE", "没有已导入的研究快照", 503)
        self.metadata = dataset.metadata_json
        self.cutoff = date.fromisoformat(self.metadata["research_cutoff"])
        self.companies_by_id = {item.id: item for item in session.scalars(select(Company))}

    def check_date(self, value: date | None):
        if value and value > self.cutoff:
            raise DomainError(
                "DATE_AFTER_CUTOFF",
                "查询日期不得晚于研究截止日",
                details={"research_cutoff": self.cutoff.isoformat()},
            )

    def health(self):
        return dict(
            status="ok",
            **{
                key: self.metadata[key]
                for key in ("dataset_version", "research_cutoff", "score_version")
            },
        )

    def require_company(self, company_id: str) -> Company:
        if company_id not in self.companies_by_id:
            raise DomainError("COMPANY_NOT_FOUND", f"公司不存在：{company_id}", 404)
        return self.companies_by_id[company_id]

    def companies(self, q: str | None = None, page: int = 1, page_size: int = 20):
        QueryFilters(q=q, page=page, page_size=page_size)
        items = sorted(
            self.companies_by_id.values(), key=lambda item: (item.display_name.casefold(), item.id)
        )
        if q:
            keyword = q.strip().casefold()
            items = [
                item
                for item in items
                if keyword
                in " ".join(
                    (item.id, item.legal_name, item.display_name, item.ticker, *item.aliases)
                ).casefold()
            ]
        return {
            "items": [serialize(item) for item in items[(page - 1) * page_size : page * page_size]],
            "total": len(items),
            "page": page,
            "page_size": page_size,
        }

    def company(self, company_id: str):
        company = self.require_company(company_id)
        relationships = self._relationships(company_id)
        distribution = dict.fromkeys(
            ("supplier", "customer", "partner", "investor_or_investee", "peer"), 0
        )
        evidence_ids, related_ids = set(), set()
        for item in relationships:
            distribution[queried_role(item, company_id)] += 1
            evidence_ids.update(link.evidence_id for link in item.evidence_links)
            related_ids.update((item.source_company_id, item.target_company_id))
        related_ids.discard(company_id)
        return dict(
            serialize(company),
            dataset=self.metadata,
            summary={
                "relationship_count": len(relationships),
                "evidence_count": len(evidence_ids),
                "related_company_count": len(related_ids),
                "distribution": distribution,
            },
        )

    def _relationships(self, company_id: str):
        self.require_company(company_id)
        return list(
            self.session.scalars(
                select(Relationship).where(
                    or_(
                        Relationship.source_company_id == company_id,
                        Relationship.target_company_id == company_id,
                    )
                )
            )
        )

    def _evidence(self, relationship: Relationship, known_at: date | None = None):
        return [
            dict(serialize(link.evidence), stance=link.stance, directness=link.directness)
            for link in relationship.evidence_links
            if not known_at
            or (link.evidence.published_at is not None and link.evidence.published_at <= known_at)
        ]

    def _visible(self, relationship: Relationship, known_at: date | None = None):
        return not known_at or any(
            item["stance"] == "supports" for item in self._evidence(relationship, known_at)
        )

    def _view(
        self, relationship: Relationship, company_id: str | None, known_at: date | None = None
    ):
        result = serialize(relationship)
        evidence = self._evidence(relationship, known_at)
        result["evidence_links"] = [
            {"evidence_id": item["id"], "stance": item["stance"], "directness": item["directness"]}
            for item in evidence
        ]
        result["source_company"] = serialize(self.companies_by_id[relationship.source_company_id])
        result["target_company"] = serialize(self.companies_by_id[relationship.target_company_id])
        related_id = (
            relationship.target_company_id
            if company_id == relationship.source_company_id
            else relationship.source_company_id
        )
        result["related_company"] = (
            serialize(self.companies_by_id[related_id]) if company_id else None
        )
        result["queried_role"] = queried_role(relationship, company_id)
        result["evidence_count"] = len(evidence)
        result["independent_source_count"] = independent_count(evidence)
        if known_at:
            if result["fact_status"] == "confirmed" and not any(
                item["stance"] == "supports" and item["directness"] == "direct" for item in evidence
            ):
                result["fact_status"] = "inferred"
                result["uncertainty"] += (
                    " 完整快照结论尚无该时点的直接支持，不能视为当时已知事实："
                    + result["business_description"]
                )
                result["business_description"] = (
                    f"截至 {known_at.isoformat()}，仅有间接依据支持 "
                    f"{result['source_company']['display_name']} 与 "
                    f"{result['target_company']['display_name']} 的候选关系；仍需直接证据。"
                )
            result["uncertainty"] += (
                f" 按 {known_at.isoformat()} 前已发表证据筛选，"
                "不表示当时已完成核验；关系描述和实体映射仍为本次研究整理。"
            )
            result["score"] = calculate_score(result, evidence, self.cutoff, datetime.now(UTC))
        else:
            result["score"] = serialize(relationship.score)
            result["score"].pop("relationship_id")
        return result

    def filtered_relationships(self, company_id: str, filters: QueryFilters):
        self.check_date(filters.known_at)
        self.check_date(filters.valid_at)
        results = []
        for item in self._relationships(company_id):
            if not self._visible(item, filters.known_at):
                continue
            if (
                filters.relationship_type
                and queried_role(item, company_id) != filters.relationship_type
            ):
                continue
            if filters.valid_at and not matches_valid_at(
                item, filters.valid_at, filters.include_unknown_time, self.cutoff
            ):
                continue
            view = self._view(item, company_id, filters.known_at)
            if filters.fact_status and view["fact_status"] != filters.fact_status:
                continue
            if view["score"]["total"] < filters.min_confidence:
                continue
            if filters.q:
                company = view["related_company"]
                haystack = " ".join(
                    (
                        company["id"],
                        company["display_name"],
                        company["legal_name"],
                        company["ticker"],
                        *company["aliases"],
                        view["business_description"],
                    )
                )
                if filters.q.strip().casefold() not in haystack.casefold():
                    continue
            if (
                filters.valid_at
                and filters.include_unknown_time
                and not matches_valid_at(item, filters.valid_at, False, self.cutoff)
            ):
                view["uncertainty"] += " 本条因包含未知时间选项纳入，无法确证在所选日期有效。"
            results.append(view)
        if filters.sort == "company_asc":
            results.sort(
                key=lambda item: (item["related_company"]["display_name"].casefold(), item["id"])
            )
        elif filters.sort == "date_desc":
            results.sort(
                key=lambda item: (
                    -(
                        date.fromisoformat(item["valid_from"]).toordinal()
                        if item["valid_from"]
                        else 0
                    ),
                    item["id"],
                )
            )
        else:
            results.sort(key=lambda item: (-item["score"]["total"], item["id"]))
        return results

    def relationships(self, company_id: str, filters: QueryFilters):
        items = self.filtered_relationships(company_id, filters)
        start = (filters.page - 1) * filters.page_size
        return {
            "items": items[start : start + filters.page_size],
            "total": len(items),
            "page": filters.page,
            "page_size": filters.page_size,
        }

    def graph(self, company_id: str, filters: QueryFilters):
        items = self.filtered_relationships(company_id, filters)
        edges = items[:100]
        node_ids = {company_id}
        for item in edges:
            node_ids.update((item["source_company_id"], item["target_company_id"]))
        return {
            "nodes": [serialize(self.companies_by_id[item]) for item in sorted(node_ids)],
            "edges": edges,
            "total": len(items),
            "displayed": len(edges),
            "truncated": len(items) > 100,
            "limit": 100,
            "scope_note": "与列表共享筛选和稳定排序，图最多展示前100条关系；列表另有分页。",
        }

    def require_relationship(self, relationship_id: str, known_at: date | None = None):
        self.check_date(known_at)
        relationship = self.session.get(Relationship, relationship_id)
        if relationship is None or not self._visible(relationship, known_at):
            raise DomainError(
                "RELATIONSHIP_NOT_FOUND", "关系不存在或在所选已公开信息范围内没有支持证据", 404
            )
        return relationship

    def relationship(self, relationship_id: str, known_at: date | None = None):
        return self._view(self.require_relationship(relationship_id, known_at), None, known_at)

    def evidence(self, relationship_id: str, known_at: date | None = None):
        items = self._evidence(self.require_relationship(relationship_id, known_at), known_at)
        return {"items": items, "total": len(items)}
