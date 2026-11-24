from fastapi import FastAPI

from app.api.v1.router import router as v1_router

app = FastAPI(
    title="StrumSpace API",
    description="Backend API for the StrumSpace guitar academy management system.",
    version="0.1.0",
)

app.include_router(v1_router)
