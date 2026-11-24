from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the StrumSpace guitar academy management system.",
    version=settings.app_version,
)

app.include_router(v1_router)
