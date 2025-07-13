from http import HTTPStatus

from fastapi import APIRouter

from .health import router as health_router
from .short import router as short_router
from .redirect import router as redirect_router
from .schemas import ErrorResponse

router: APIRouter = APIRouter(
    responses={
        HTTPStatus.BAD_REQUEST: {"model": ErrorResponse},
        HTTPStatus.UNAUTHORIZED: {"model": ErrorResponse},
        HTTPStatus.FORBIDDEN: {"model": ErrorResponse},
        HTTPStatus.NOT_FOUND: {"model": ErrorResponse},
        HTTPStatus.CONFLICT: {"model": ErrorResponse},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    }
)
router.include_router(health_router)
router.include_router(short_router)
router.include_router(redirect_router)

__all__ = ["router"]
