import hashlib
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import Field, HttpUrl, field_validator, model_validator

from .common import Identifier, StrictModel, Text


class EvidenceData(StrictModel):
    id: Identifier
    title: Text
    source_url: HttpUrl
    publisher: Text
    published_at: date | None
    retrieved_at: datetime
    evidence_locator: Text
    excerpt: Text
    interpretation: Text
    source_type: Literal["regulatory", "company", "media"]
    independence_key: Text
    content_sha256: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    access_restrictions: Text
    redistribution_notes: Text

    @field_validator("retrieved_at")
    @classmethod
    def aware_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("retrieved_at 必须包含时区")
        return value

    @model_validator(mode="after")
    def verify_content(self):
        actual = hashlib.sha256(self.excerpt.encode("utf-8")).hexdigest()
        if self.content_sha256 != actual:
            raise ValueError(f"证据 {self.id} 摘录 SHA-256 不匹配")
        if self.published_at and self.published_at > self.retrieved_at.date():
            raise ValueError("发布日期不能晚于实际获取日期")
        return self


class EvidenceLinkData(StrictModel):
    evidence_id: Identifier
    stance: Literal["supports", "contradicts"]
    directness: Literal["direct", "indirect"]
