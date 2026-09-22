from datetime import date
from typing import Annotated

from pydantic import Field

from .common import FactStatus, Role, SortOrder, StrictModel


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
