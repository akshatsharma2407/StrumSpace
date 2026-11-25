import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
    unexpected_exception_handler,
)
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.db.engine import dispose_engine, verify_database_connection


configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting application")
    await verify_database_connection()
    try:
        yield
    finally:
        await dispose_engine()
        logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the StrumSpace guitar academy management system.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unexpected_exception_handler)

app.include_router(v1_router)
