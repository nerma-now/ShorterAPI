from http import HTTPStatus

from typing import Annotated, Optional, Dict, Any, Sequence

from fastapi import APIRouter, Header, Body, Path, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.routers.schemas import Response, ErrorResponse, Message

from infrastructure.database import database
from infrastructure.database.models import Short
from infrastructure.database.crud import ShortRepository

from .service import Service
from .schemas import BaseShort, CreateShort, SingleGetShort, FullGetShort, UpdateShort


router: APIRouter = APIRouter(
    prefix="/short",
    tags=["short"]
)


@router.post(
    path="/",
    response_model=Response,
    status_code=HTTPStatus.CREATED,
    summary="Create a short URL",
    description="""
        Creates a new short URL entry with either:
        - A custom specified code
        - An automatically generated code

        Validations:
        - Custom codes must be unique
        - URLs must be valid
        """,
    response_description="Details of created short URL"
)
async def create_short(session: Annotated[AsyncSession, Depends(database.session)],
                       model: Annotated[CreateShort, Body()]) -> Response:
    """
    Endpoint to create shortened URL entries.

    Args:
        session: Database session from dependency
        model: Request body containing URL details

    Returns:
        Response with created short URL details

    Raises:
        HTTPException 409: If custom code already exists
        HTTPException 422: If URL validation fails
    """

    if model.code is not None:
        exists: Optional[Short] = await ShortRepository().get(session=session, target=Short.code, value=model.code)

        if exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=ErrorResponse(
                    detail=[Message(msg="The code is busy")]
                ).model_dump()
            )

    if model.code is None:
        code: str = await Service().generate_code(session=session)
        model.code = code

    data: Dict[str, Any] = model.model_dump()
    data["url"] = str(model.url)

    short: Optional[Short] = await ShortRepository().add(session=session, target=Short(**data))

    return Response(
        detail=[Message(msg="Short URL created")],
        content=[BaseShort.model_validate(short)]
    )


@router.get(
    path="/",
    response_model=Response,
    status_code=HTTPStatus.OK,
    summary="Retrieve all short URLs",
    description="""
    Returns all existing short URL mappings in the system.

    Responses:
    - 200 OK: Returns list of short URLs
    - 404 Not Found: If no short URLs exist in the system
    """,
    response_description="List of short URL entries"
)
async def get_shorts(session: Annotated[AsyncSession, Depends(database.session)]) -> Response:
    """
    Retrieve paginated list of all short URLs.

        Args:
            session: Database session from dependency

        Returns:
            Response containing list of short URLs

        Raises:
            HTTPException 404: If no short URLs exist
        """

    shorts: Sequence[Short] = await ShortRepository().get_all(session=session)

    if not shorts:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorResponse(
                detail=[Message(msg="There are no available links created")]
            ).model_dump()
        )

    return Response(
        detail=[Message(msg="Short URLs received")],
        content=[BaseShort.model_validate(short) for short in shorts]
    )


@router.get(
    path="/lookup",
    response_model=Response,
    status_code=HTTPStatus.OK,
    summary="Retrieve a short URL by ID or code",
    description="""
    Returns details for a specific short URL

    Note: Must provide either id or code parameter, but not both.

    Responses:
    - 200 OK: Returns the requested short URL details
    - 400 Bad Request: If neither id nor code is provided
    - 404 Not Found: If no matching short URL exists
    """,
    response_description="Short URL details"
)
async def get_short(session: Annotated[AsyncSession, Depends(database.session)],
                    model: Annotated[FullGetShort, Header()]) -> Response:
    """Retrieve details for a short URL by either ID or code.

    Args:
        session: Database session
        id: UUID of the short URL (optional)
        code: Short code of the URL (optional)

    Returns:
        Response containing the short URL details if found

    Raises:
        HTTPException 400: If neither id nor code is provided
        HTTPException 404: If no matching short URL exists
    """
    short: Optional[Short] = None

    if model.id is not None:
        short = await ShortRepository().get(session=session, target=Short.id, value=model.id)
    elif model.code is not None:
        short = await ShortRepository().get(session=session, target=Short.code, value=model.code)
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorResponse(
                detail=[Message(msg="No id and code for get object")]
            ).model_dump()
        )


    if not short:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorResponse(
                detail=[Message(msg="Short link with such ID does not exist")]
            ).model_dump()
        )

    return Response(
        detail=[Message(msg="Short URL received")],
        content=[BaseShort.model_validate(short)]
    )


@router.delete(
    path="/",
    response_model=Response,
    status_code=HTTPStatus.OK,
    summary="Delete all short URLs",
    description="""
    **DANGER**: Permanently deletes ALL short URLs in the system.
    
    Responses:
    - 200 OK: Returns list of deleted short URLs
    - 404 No Content: If no short URLs existed
    """,
    response_description="List of deleted short URL entries"
)
async def delete_shorts(session: Annotated[AsyncSession, Depends(database.session)]) -> Response:
    """
    Permanently delete all short URL records.

   Args:
       session: Database session from dependency

   Returns:
       Response containing list of deleted short URLs

   Raises:
       HTTPException 404: If no short URLs existed
   """

    shorts: Sequence[Short] = await ShortRepository().get_all(session=session)

    if not shorts:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorResponse(
                detail=[Message(msg="There are no available links created")]
            ).model_dump()
        )

    for short in shorts:
        await ShortRepository().delete(session=session, target=short)

    return Response(
        detail=[Message(msg="Short URLs deleted")],
        content=[BaseShort.model_validate(short) for short in shorts]
    )


@router.delete(
    path="/{id}",
    response_model=Response,
    status_code=HTTPStatus.OK,
    summary="Delete a specific short URL",
    description="""
    Permanently deletes a short URL by its unique identifier.

    Responses:
    - 200 OK: Returns details of the deleted short URL
    - 404 Not Found: If no short URL exists with the specified ID
    """,
    response_description="Details of deleted short URL"
)
async def delete_short(session: Annotated[AsyncSession, Depends(database.session)],
                       model: Annotated[SingleGetShort, Path()]) -> Response:
    """
    Delete a specific short URL entry.

    Args:
        session: Database session from dependency
        id: UUID of the short URL to delete

    Returns:
        Response containing details of the deleted short URL

    Raises:
        HTTPException 404: If no short URL exists with the specified ID
    """

    short: Optional[Short] = await ShortRepository().get(session=session, target=Short.id, value=model.id)

    if not short:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorResponse(
                detail=[Message(msg="Short link with such ID does not exist")]
            ).model_dump()
        )

    await ShortRepository().delete(session=session, target=short)

    return Response(
        detail=[Message(msg="Short URL deleted")],
        content=[BaseShort.model_validate(short)]
    )


@router.put(
    path="/{id}",
    response_model=Response,
    status_code=HTTPStatus.OK,
    summary="Update a short URL",
    description="""
    Updates properties of an existing short URL.

    Validations:
    - At least one field must be provided for update
    - Code must remain unique if changed
    - URL must be valid
    """,
    response_description="Updated short URL details"
)
async def update_short(session: Annotated[AsyncSession, Depends(database.session)],
                       model: Annotated[SingleGetShort, Header()],
                       updated_model: Annotated[UpdateShort, Body()]) -> Response:
    """Update an existing short URL entry.

    Args:
        session: Database session
        id: UUID of short URL to update
        update_data: Fields to update (only non-null fields will be applied)

    Returns:
        Response with updated short URL details

    Raises:
        HTTPException 400: If no valid fields provided
        HTTPException 404: If short URL not found
        HTTPException 409: If new code already exists
    """

    short: Optional[Short] = await ShortRepository().get(session=session, target=Short.id, value=model.id)

    if not short:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorResponse(
                detail=[Message(msg="Short link with such ID does not exist")]
            ).model_dump()
        )

    if not updated_model.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorResponse(
                detail=[Message(msg="No fields provided for update")]
            ).model_dump()
        )

    short_unique: Optional[Short] = await ShortRepository().get(session=session, target=Short.code, value=updated_model.code)
    if short_unique:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=ErrorResponse(
                detail=[Message(msg="The code is busy")]
            ).model_dump()
        )

    short = await ShortRepository().update(
        session=session,
        instance=short,
        **updated_model.model_dump(exclude_unset=True)
    )

    return Response(
        detail=[Message(msg="Short URL updated")],
        content=[BaseShort.model_validate(short)]
    )
