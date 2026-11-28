from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated, Generic, Literal, TypeVar
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

IST = ZoneInfo("Asia/Kolkata")
_PHONE_PATTERN = re.compile(r"^(?:\+91)?([6-9][0-9]{9})$")
EmailValue = Annotated[EmailStr, Field(max_length=254)]

EnquiryStatus = Literal["NEW", "CONTACTED", "INTERESTED", "NOT_INTERESTED", "CLOSED"]
ExperienceLevel = Literal["BEGINNER", "INTERMEDIATE", "ADVANCED"]
EnquirySortField = Literal["CREATED_AT", "UPDATED_AT", "NEXT_FOLLOW_UP_AT"]
SortOrder = Literal["ASC", "DESC"]


class EnquiryBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: Annotated[str, Field(min_length=1, max_length=100)]
    phone_number: str
    email: EmailValue | None = None
    age: Annotated[int | None, Field(gt=5, le=120)] = None
    experience_level: ExperienceLevel | None = None
    message: Annotated[str | None, Field(max_length=1000)] = None

    @field_validator("full_name", mode="before")
    @classmethod
    def normalize_full_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone_number(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        compact = re.sub(r"\s+", "", value.strip())
        match = _PHONE_PATTERN.fullmatch(compact)
        if not match:
            raise ValueError("Enter a valid Indian mobile number")
        return f"+91{match.group(1)}"

    @field_validator("email", "message", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value


class EnquiryCreate(EnquiryBase):
    pass


def _require_aware_ist(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Datetime must include a timezone offset")
    return value.astimezone(IST)


class EnquiryVisitorUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    phone_number: str | None = None
    email: EmailValue | None = None
    age: Annotated[int | None, Field(gt=5, le=120)] = None
    experience_level: ExperienceLevel | None = None
    message: Annotated[str | None, Field(max_length=1000)] = None

    @model_validator(mode="before")
    @classmethod
    def reject_empty_update(cls, value: object) -> object:
        if isinstance(value, dict):
            if not value:
                raise ValueError("At least one field is required")
            if "full_name" in value and value["full_name"] is None:
                raise ValueError("full_name cannot be null")
            if "phone_number" in value and value["phone_number"] is None:
                raise ValueError("phone_number cannot be null")
        return value

    @field_validator("full_name", mode="before")
    @classmethod
    def normalize_full_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone_number(cls, value: object) -> object:
        if value is None:
            return value
        return EnquiryBase.normalize_phone_number(value)

    @field_validator("email", "message", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        return EnquiryBase.normalize_optional_text(value)


class EnquiryInternalUpdate(EnquiryVisitorUpdate):
    status: EnquiryStatus | None = None
    last_contacted_at: datetime | None = None
    next_follow_up_at: datetime | None = None

    @field_validator("last_contacted_at", "next_follow_up_at")
    @classmethod
    def normalize_datetime(cls, value: datetime | None) -> datetime | None:
        return _require_aware_ist(value)

    @model_validator(mode="after")
    def validate_follow_up_relationship(self) -> EnquiryInternalUpdate:
        now = datetime.now(IST)
        if self.last_contacted_at is not None and self.last_contacted_at > now:
            raise ValueError("last_contacted_at cannot be in the future")
        if (
            self.last_contacted_at is not None
            and self.next_follow_up_at is not None
            and self.next_follow_up_at <= self.last_contacted_at
        ):
            raise ValueError("next_follow_up_at must be after last_contacted_at")
        return self


class EnquiryVisitorResponse(EnquiryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: EnquiryStatus
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def serialize_datetime_as_ist(cls, value: datetime) -> datetime:
        return _require_aware_ist(value)
    

class EnquiryInternalResponse(EnquiryVisitorResponse):
    last_contacted_at: datetime | None = None
    next_follow_up_at: datetime | None = None

    @field_validator("last_contacted_at", "next_follow_up_at")
    @classmethod
    def serialize_follow_up_as_ist(cls, value: datetime | None) -> datetime | None:
        return _require_aware_ist(value)


ResponseT = TypeVar("ResponseT", bound=BaseModel)


class EnquiryListResponse(BaseModel, Generic[ResponseT]):
    model_config = ConfigDict(from_attributes=True)

    items: list[ResponseT]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)


class EnquiryListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: EnquiryStatus | None = None
    experience_level: ExperienceLevel | None = None
    search: Annotated[str | None, Field(max_length=254)] = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    next_follow_up_from: datetime | None = None
    next_follow_up_to: datetime | None = None
    sort_by: EnquirySortField = "CREATED_AT"
    order: SortOrder = "DESC"
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @field_validator("search", mode="before")
    @classmethod
    def normalize_search(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @field_validator("created_from", "created_to", "next_follow_up_from", "next_follow_up_to")
    @classmethod
    def normalize_query_datetime(cls, value: datetime | None) -> datetime | None:
        return _require_aware_ist(value)

    @model_validator(mode="after")
    def validate_date_ranges(self) -> EnquiryListQuery:
        ranges = (
            (self.created_from, self.created_to, "created"),
            (self.next_follow_up_from, self.next_follow_up_to, "next_follow_up"),
        )
        for lower, upper, name in ranges:
            if lower is not None and upper is not None and lower > upper:
                raise ValueError(f"{name}_from must be before or equal to {name}_to")
        return self


class EnquiryIdPath(BaseModel):
    id: int = Field(gt=0)
