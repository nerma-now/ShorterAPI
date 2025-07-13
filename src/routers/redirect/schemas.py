from typing import Annotated
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, Field


class GetShort(BaseModel):
    """Model for get short URL object"""

    code: Annotated[str, MinLen(1), MaxLen(6)] = Field(
        ...,
        description="Short code for the URL"
    )

class UrlShort(BaseModel):
    """Model for get original long URL object"""

    url: str = Field(
        ...,
        description="Original long URL"
    )


__all__ = ["GetShort", "UrlShort"]
