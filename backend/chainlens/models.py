"""SQLAlchemy models. Evidence links carry the stance for each particular conclusion."""

from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    __tablename__ = "datasets"
    version: Mapped[str] = mapped_column(String, primary_key=True)
    content_sha256: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    legal_name: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    aliases: Mapped[list] = mapped_column(JSON)
    ticker: Mapped[str] = mapped_column(String)
    exchange: Mapped[str] = mapped_column(String)
    listing_status: Mapped[str] = mapped_column(String)
    parent_id: Mapped[str | None] = mapped_column(ForeignKey("companies.id"))
    identity_notes: Mapped[str] = mapped_column(Text)


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
    evidence_links: Mapped[list["RelationshipEvidence"]] = relationship(
        cascade="all, delete-orphan", lazy="selectin", order_by="RelationshipEvidence.evidence_id"
    )
    score: Mapped["Score"] = relationship(
        cascade="all, delete-orphan", lazy="joined", uselist=False
    )


class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text)
    publisher: Mapped[str] = mapped_column(String)
    published_at: Mapped[date | None] = mapped_column(Date)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    evidence_locator: Mapped[str] = mapped_column(Text)
    excerpt: Mapped[str] = mapped_column(Text)
    interpretation: Mapped[str] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String)
    independence_key: Mapped[str] = mapped_column(String, index=True)
    content_sha256: Mapped[str] = mapped_column(String)
    access_restrictions: Mapped[str] = mapped_column(Text)
    redistribution_notes: Mapped[str] = mapped_column(Text)


class RelationshipEvidence(Base):
    __tablename__ = "relationship_evidence"
    relationship_id: Mapped[str] = mapped_column(ForeignKey("relationships.id"), primary_key=True)
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence.id"), primary_key=True)
    stance: Mapped[str] = mapped_column(String)
    directness: Mapped[str] = mapped_column(String)
    evidence: Mapped[Evidence] = relationship(lazy="joined")


class Score(Base):
    __tablename__ = "scores"
    relationship_id: Mapped[str] = mapped_column(ForeignKey("relationships.id"), primary_key=True)
    total: Mapped[int] = mapped_column(Integer)
    rule_version: Mapped[str] = mapped_column(String)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    components: Mapped[list] = mapped_column(JSON)
    explanation: Mapped[str] = mapped_column(Text)
    current_validity: Mapped[str] = mapped_column(String)
