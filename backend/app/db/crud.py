"""Database reads shared by research queries and snapshot initialization."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import Company, Dataset, Relationship


def get_active_dataset(session: Session) -> Dataset | None:
    return session.scalar(select(Dataset).where(Dataset.active.is_(True)))


def list_companies(session: Session) -> list[Company]:
    return list(session.scalars(select(Company)))


def list_company_relationships(session: Session, company_id: str) -> list[Relationship]:
    return list(
        session.scalars(
            select(Relationship).where(
                or_(
                    Relationship.source_company_id == company_id,
                    Relationship.target_company_id == company_id,
                )
            )
        )
    )


def get_relationship(session: Session, relationship_id: str) -> Relationship | None:
    return session.get(Relationship, relationship_id)
