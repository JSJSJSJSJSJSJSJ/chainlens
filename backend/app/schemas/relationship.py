from datetime import date
from typing import Literal

from pydantic import model_validator

from .common import FactStatus, Identifier, RelationshipType, StrictModel, Text
from .evidence import EvidenceLinkData


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
