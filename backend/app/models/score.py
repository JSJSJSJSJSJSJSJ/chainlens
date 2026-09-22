from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Score(Base):
    __tablename__ = "scores"
    relationship_id: Mapped[str] = mapped_column(ForeignKey("relationships.id"), primary_key=True)
    total: Mapped[int] = mapped_column(Integer)
    rule_version: Mapped[str] = mapped_column(String)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    components: Mapped[list] = mapped_column(JSON)
    explanation: Mapped[str] = mapped_column(Text)
    current_validity: Mapped[str] = mapped_column(String)
