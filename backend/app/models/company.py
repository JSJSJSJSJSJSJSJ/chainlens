from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


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
