from typing import List

from pydantic import Field, BaseModel


class CORSConfig(BaseModel):
    """
    Configuration model for Cross-Origin Resource Sharing (CORS) settings.

    Attributes:
        origins: List of allowed origins (default: ["*"])
        methods: List of allowed HTTP methods (default: ["GET", "POST"])
        headers: List of allowed headers (default: ["*"])
        credentials: Allow credentials (cookies, auth headers) (default: False)
        max_age: Maximum age (seconds) for CORS preflight cache (default: 3600)
    """

    origins: List[str] = Field(default=["*"])
    methods: List[str] = Field(default=["GET", "POST"])
    headers: List[str] = Field(default=["*"])
    credentials: bool = Field(default=False)
    max_age: int = Field(default=3600)


__all__ = ["CORSConfig"]
