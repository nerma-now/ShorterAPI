from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse

from .config import config
from .routers import router

app: FastAPI = FastAPI(
    debug=config.debug,
    title=config.title,
    description=config.description,
    default_response_class=JSONResponse,
    docs_url=config.docs_url,
    redoc_url=config.redoc_url
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins,
    allow_credentials=config.cors.credentials,
    allow_methods=config.cors.methods,
    allow_headers=config.cors.headers,
    max_age=config.cors.max_age
)
app.include_router(router)

__all__ = ["app"]
