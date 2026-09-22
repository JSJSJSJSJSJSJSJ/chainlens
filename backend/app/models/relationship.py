from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.evidence import Evidence
    from app.models.score import Score


class Relationship(Base):
    __tablename__ = "relationships"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True)
    target_company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True)
    relationship_type: Mapped[str] = mapped_column(String, index=True)
    business_description: Mapped[str] = mapped_column(Text)
    fact_status: Mapped[str] = mapped_column(String)
    valid_from: Mapped[date | None] = mapped_column(Date)
    valid_to: Mapped[date | None] = mapped_column(Date)
    temporal_status: Mapped[str] = mapped_column(String)
    continuity_note: Mapped[str] = mapped_column(Text)
    uncertainty: Mapped[str] = mapped_column(Text)
    human_review_status: Mapped[str] = mapped_column(String)
    entity_resolution: Mapped[str] = mapped_column(String)
    comparison_dimension: Mapped[str | None] = mapped_column(Text)
    quantitative_context: Mapped[str | None] = mapped_column(Text)
    evidence_links: Mapped[list[RelationshipEvidence]] = relationship(
        cascade="all, delete-orphan", lazy="selectin", order_by="RelationshipEvidence.evidence_id"
    )
    score: Mapped[Score] = relationship(cascade="all, delete-orphan", lazy="joined", uselist=False)


class RelationshipEvidence(Base):
    __tablename__ = "relationship_evidence"
    relationship_id: Mapped[str] = mapped_column(ForeignKey("relationships.id"), primary_key=True)
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence.id"), primary_key=True)
    stance: Mapped[str] = mapped_column(String)
    directness: Mapped[str] = mapped_column(String)
    evidence: Mapped[Evidence] = relationship(lazy="joined")
