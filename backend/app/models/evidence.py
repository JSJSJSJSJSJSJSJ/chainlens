from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


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
