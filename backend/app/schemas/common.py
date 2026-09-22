from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Identifier = Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9_-]*$", min_length=1, max_length=100)]
Text = Annotated[str, Field(min_length=1)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RelationshipType(StrEnum):
    supplier = "supplier"
    partner = "partner"
    investor_or_investee = "investor_or_investee"
    peer = "peer"


class Role(StrEnum):
    supplier = "supplier"
    customer = "customer"
    partner = "partner"
    investor_or_investee = "investor_or_investee"
    peer = "peer"


class FactStatus(StrEnum):
    confirmed = "confirmed"
    inferred = "inferred"
    unknown = "unknown"


class SortOrder(StrEnum):
    confidence_desc = "confidence_desc"
    company_asc = "company_asc"
    date_desc = "date_desc"
