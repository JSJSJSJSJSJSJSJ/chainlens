from datetime import date, datetime
from typing import Literal

from pydantic import field_validator, model_validator

from .common import StrictModel, Text
from .company import CompanyData
from .evidence import EvidenceData
from .relationship import RelationshipData


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
