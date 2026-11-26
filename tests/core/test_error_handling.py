from fastapi import FastAPI
from httpx import AsyncClient

from app.main import app


async def test_unknown_route_uses_standard_error_response(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "HTTP_404",
            "message": "Not Found",
            "details": None,
        }
    }


def test_fastapi_application_is_constructed() -> None:
    assert isinstance(app, FastAPI)
