from http import HTTPStatus

from fastapi import APIRouter

from src.routers.schemas import Response, Message

router: APIRouter = APIRouter(
    prefix='/healths',
    tags=['healths']
)


@router.get(
    path='/',
    response_model=Response,
    status_code=HTTPStatus.OK,
    summary="Check service health",
    description="Health check endpoint",
    response_description="Service status confirmation"
)
def get_health() -> Response:
    """
    Endpoint to verify service availability.

    Returns:
        Response: Standard response with health status message
    """

    return Response(
        detail=[Message(msg="Service is alive")]
    )
