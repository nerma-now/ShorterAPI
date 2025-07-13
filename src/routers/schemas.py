from typing import List, Optional, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Basic message container for API responses.

    Attributes:
        msg: The message content
    """

    msg: str


class BaseResponse(BaseModel):
    """
    Base structure for all API responses.

    Attributes:
        success: Overall operation status
        detail: Optional list of message objects
        content: Optional list of response data
    """

    success: bool
    detail: Optional[List[Message]] = Field(default=None)
    content: Optional[List[Any]] = Field(default=None)


class Response(BaseResponse):
    """
    Standard success response structure
    """

    success: bool = Field(default=True)


class ErrorResponse(BaseResponse):
    """
    Standard error response structure
    """

    success: bool = Field(default=False)


__all__ = ["Message", "Response", "ErrorResponse"]