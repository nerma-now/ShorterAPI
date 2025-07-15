import uuid

from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class BaseShort(BaseModel):
    """Base model for shortened URL representation"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        ...,
        description="Unique identifier for the short URL"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the short URL was created"
    )
    last_updated_at: datetime = Field(
        ...,
        description="Timestamp when the short URL was last updated"
    )
    is_activated: bool = Field(
        ...,
        description="Whether the short URL is active and can be used"
    )
    code: Optional[Annotated[str, MinLen(1), MaxLen(6)]] = Field(
        ...,
        description="Short code for the URL"
    )
    url: str = Field(
        ...,
        description="Original long URL"
    )
    expires_at: Optional[datetime] = Field(
        ...,
        description="Optional expiration datetime (UTC)"
    )

class UpdateShort(BaseModel):
    """Model for update short URL object"""

    model_config = ConfigDict(extra="forbid")

    is_activated: Optional[bool] = Field(
        default=None,
        description="Whether the short URL is active and can be used"
    )
    code: Optional[Annotated[str, MinLen(1), MaxLen(6)]] = Field(
        default=None,
        description="Short code for the URL"
    )
    url: Optional[str] = Field(
        default=None,
        description="Original long URL"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="Optional expiration datetime (UTC)"
    )

class GetShortByID(BaseModel):
    """Model for get short URL object using ID"""

    id: uuid.UUID = Field(
        ...,
        description="Unique identifier for the short URL"
    )

class CreateShort(BaseModel):
    """Model for creating short URL with optional custom code and expiration."""

    code: Optional[Annotated[str, MinLen(1), MaxLen(6)]] = Field(
        default=None,
        description="Custom short code (1-6 chars). Leave None for auto-generation"
    )
    url: HttpUrl = Field(
        ...,
        description="Original URL to shorten (must include http/https)"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="Optional expiration datetime (UTC)"
    )


__all__ = ["BaseShort", "UpdateShort", "GetShortByID", "CreateShort"]
