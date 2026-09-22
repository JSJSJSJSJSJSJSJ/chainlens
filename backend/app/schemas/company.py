from typing import Literal

from .common import Identifier, StrictModel, Text


class CompanyData(StrictModel):
    id: Identifier
    legal_name: Text
    display_name: Text
    aliases: list[str]
    ticker: Text
    exchange: Text
    listing_status: Literal["listed"]
    parent_id: Identifier | None
    identity_notes: Text
