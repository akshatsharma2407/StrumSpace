from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.db.engine import dispose_engine, verify_database_connection


@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    await verify_database_connection()
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the StrumSpace guitar academy management system.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(v1_router)
