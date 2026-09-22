"""Request-scoped database sessions and shared query dependencies."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Query, Request
from sqlalchemy.orm import Session

from app.schemas.query import QueryFilters
from app.services.research_service import ResearchService


def get_session(request: Request) -> Iterator[Session]:
    with Session(request.app.state.engine) as session:
        yield session


def get_research_service(session: Annotated[Session, Depends(get_session)]) -> ResearchService:
    return ResearchService(session)


Service = Annotated[ResearchService, Depends(get_research_service)]
Filters = Annotated[QueryFilters, Query()]
