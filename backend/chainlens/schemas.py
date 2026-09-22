"""The checked-in snapshot is an untrusted input, validated before any database write."""

import hashlib
from datetime import date, datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator

Identifier = Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9_-]*$", min_length=1, max_length=100)]
Text = Annotated[str, Field(min_length=1)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RelationshipType(StrEnum):
    supplier = "supplier"
    partner = "partner"
    investor_or_investee = "investor_or_investee"
    peer = "peer"


class Role(StrEnum):
    supplier = "supplier"
    customer = "customer"
    partner = "partner"
    investor_or_investee = "investor_or_investee"
    peer = "peer"


class FactStatus(StrEnum):
    confirmed = "confirmed"
    inferred = "inferred"
    unknown = "unknown"


class SortOrder(StrEnum):
    confidence_desc = "confidence_desc"
    company_asc = "company_asc"
    date_desc = "date_desc"


class Metadata(StrictModel):
    dataset_version: Text
    research_cutoff: date
    score_version: Literal["1.0.0"]
    created_at: datetime
    description: Text
    gaps: list[str]

    @field_validator("created_at")
    @classmethod
    def aware_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("created_at 必须包含时区")
        return value


class CompanyData(StrictModel):
    id: Identifier
    legal_name: Text
    display_name: Text
    aliases: list[str]
    ticker: Text
    exchange: Text
    listing_status: Literal["listed"]
    parent_id: Identifier | None
    identity_notes: Text


class EvidenceData(StrictModel):
    id: Identifier
    title: Text
    source_url: HttpUrl
    publisher: Text
    published_at: date | None
    retrieved_at: datetime
    evidence_locator: Text
    excerpt: Text
    interpretation: Text
    source_type: Literal["regulatory", "company", "media"]
    independence_key: Text
    content_sha256: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    access_restrictions: Text
    redistribution_notes: Text

    @field_validator("retrieved_at")
    @classmethod
    def aware_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("retrieved_at 必须包含时区")
        return value

    @model_validator(mode="after")
    def verify_content(self):
        actual = hashlib.sha256(self.excerpt.encode("utf-8")).hexdigest()
        if self.content_sha256 != actual:
            raise ValueError(f"证据 {self.id} 摘录 SHA-256 不匹配")
        if self.published_at and self.published_at > self.retrieved_at.date():
            raise ValueError("发布日期不能晚于实际获取日期")
        return self


class EvidenceLinkData(StrictModel):
    evidence_id: Identifier
    stance: Literal["supports", "contradicts"]
    directness: Literal["direct", "indirect"]


class RelationshipData(StrictModel):
    id: Identifier
    source_company_id: Identifier
    target_company_id: Identifier
    relationship_type: RelationshipType
    business_description: Text
    fact_status: FactStatus
    valid_from: date | None
    valid_to: date | None
    temporal_status: Literal["historical", "current", "unknown"]
    continuity_note: Text
    uncertainty: Text
    human_review_status: Literal["pending"]
    entity_resolution: Literal["exact", "mapped", "uncertain"]
    comparison_dimension: str | None
    quantitative_context: str | None
    evidence_links: list[EvidenceLinkData]

    @model_validator(mode="after")
    def semantic_constraints(self):
        if self.source_company_id == self.target_company_id:
            raise ValueError("不允许自身关系")
        if self.valid_from and self.valid_to and self.valid_from > self.valid_to:
            raise ValueError("valid_from 不得晚于 valid_to")
        if self.relationship_type == RelationshipType.peer and not self.comparison_dimension:
            raise ValueError("peer 必须说明比较业务维度")
        if len({link.evidence_id for link in self.evidence_links}) != len(self.evidence_links):
            raise ValueError("同一关系不能重复引用同一证据")
        if self.fact_status == FactStatus.confirmed and not any(
            link.stance == "supports" and link.directness == "direct"
            for link in self.evidence_links
        ):
            raise ValueError("confirmed 必须具有直接支持证据")
        return self


class Snapshot(StrictModel):
    metadata: Metadata
    companies: list[CompanyData]
    evidence: list[EvidenceData]
    relationships: list[RelationshipData]

    @model_validator(mode="after")
    def references_and_dates(self):
        for label in ("companies", "evidence", "relationships"):
            values = getattr(self, label)
            if len({item.id for item in values}) != len(values):
                raise ValueError(f"{label} 包含重复 ID")
        companies = {item.id: item for item in self.companies}
        evidence_ids = {item.id for item in self.evidence}
        cutoff = self.metadata.research_cutoff
        for company in self.companies:
            if company.parent_id and company.parent_id not in companies:
                raise ValueError(f"{company.id} 的母公司引用不存在")
            seen = {company.id}
            parent = company.parent_id
            while parent:
                if parent not in companies:
                    raise ValueError(f"母公司引用不存在：{parent}")
                if parent in seen:
                    raise ValueError("母子公司映射存在循环")
                seen.add(parent)
                parent = companies[parent].parent_id
        for evidence in self.evidence:
            if evidence.published_at and evidence.published_at > cutoff:
                raise ValueError(f"{evidence.id} 发布日期晚于研究截止日")
        for relationship in self.relationships:
            if (
                not {relationship.source_company_id, relationship.target_company_id}
                <= companies.keys()
            ):
                raise ValueError(f"{relationship.id} 引用不存在的公司")
            if not {link.evidence_id for link in relationship.evidence_links} <= evidence_ids:
                raise ValueError(f"{relationship.id} 引用不存在的证据")
            if relationship.valid_from and relationship.valid_from > cutoff:
                raise ValueError("不能将截止日后的关系作为已发生事实导入")
        return self


class QueryFilters(StrictModel):
    q: Annotated[str, Field(max_length=200)] | None = None
    relationship_type: Role | None = None
    min_confidence: Annotated[int, Field(ge=0, le=100)] = 0
    fact_status: FactStatus | None = None
    known_at: date | None = None
    valid_at: date | None = None
    include_unknown_time: bool = False
    page: Annotated[int, Field(ge=1)] = 1
    page_size: Annotated[int, Field(ge=1, le=100)] = 20
    sort: SortOrder = SortOrder.confidence_desc
