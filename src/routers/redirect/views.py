from http import HTTPStatus

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Request, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette.responses import RedirectResponse

from src.routers.schemas import ErrorResponse, Message, Response

from infrastructure.database import database
from infrastructure.database.models import Short
from infrastructure.database.crud import ShortRepository

from .schemas import GetShortByCode, ResponseShort

router: APIRouter = APIRouter(
    prefix="/redirects",
    tags=["redirects"]
)


@router.get(
    path="/{code}",
    response_model=Response | None,
    responses={
        HTTPStatus.TEMPORARY_REDIRECT: {
            "description": "Temporary Redirect",
            "headers": {
                "Location": {
                    "description": "URL to redirect to",
                    "type": "string"
                }
            }
        },
    },
    status_code=HTTPStatus.OK,
    description="""Handles short URL redirection with content negotiation.
    
    Behavior:
    - Returns JSON response if 'Accept: application/json' header present
    - Performs 307 redirect to original URL by default
    """
)
async def get_redirect(session: Annotated[AsyncSession, Depends(database.session)],
                       model: Annotated[GetShortByCode, Path()],
                       request: Request) -> Response | RedirectResponse:
    """Handle short URL redirection with content negotiation.

    Args:
        session: Database session
        code: Short code for the URL
        request: Original request for header inspection

    Returns:
        JSON response if client accepts JSON, otherwise performs redirect

    Raises:
        HTTPException 404: If short code doesn't exist
    """

    short: Optional[Short] = await ShortRepository().get(session=session, target=Short.code, value=model.code)

    if not short:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorResponse(
                detail=[Message(msg="Short link with such code does not exist")]
            ).model_dump()
        )

    model: ResponseShort = ResponseShort.model_validate(short)

    if request.headers.get("accept") == "application/json":
        return Response(
            detail=[Message(msg="Original URL received")],
            content=[model]
        )

    return RedirectResponse(
        url=short.url,
        status_code=HTTPStatus.TEMPORARY_REDIRECT,
        headers={"Location": model.url}
    )
