import uuid

from typing import Annotated
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, Field, ConfigDict


class GetShortByCode(BaseModel):
    """Model for get short URL object"""

    code: Annotated[str, MinLen(1), MaxLen(6)] = Field(
        ...,
        description="Short code for the URL"
    )

class ResponseShort(BaseModel):
    """Model for getting ID and long URL of an object"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        ...,
        description="Unique identifier for the short URL"
    )
    url: str = Field(
        ...,
        description="Original long URL"
    )


__all__ = ["GetShortByCode", "ResponseShort"]
