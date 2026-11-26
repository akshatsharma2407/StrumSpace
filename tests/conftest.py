from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.core.config import Settings
from app.core.config import TestDatabaseSettings as DatabaseTestSettings
from app.db.engine import create_database_engine
from app.main import app


TestDatabaseConfig = DatabaseTestSettings


@pytest.fixture(scope="session")
def test_database_settings() -> TestDatabaseConfig:
    database_settings = TestDatabaseConfig()
    development_settings = Settings()
    if database_settings.database_name == development_settings.database_name:
        raise RuntimeError("Test database must be different from the development database")
    if database_settings.database_user == development_settings.database_user:
        raise RuntimeError("Test database user must be different from the development database user")
    return database_settings


@pytest.fixture(scope="session")
async def test_engine(test_database_settings: TestDatabaseConfig) -> AsyncIterator[AsyncEngine]:
    engine = create_database_engine(test_database_settings)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="session")
def test_session_factory(
    test_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest.fixture
async def db_session(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with test_session_factory() as session:
        yield session


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_database_name(
    db_session: AsyncSession,
    test_database_settings: TestDatabaseConfig,
) -> str:
    result = await db_session.execute(text("SELECT DATABASE()"))
    database_name = result.scalar_one()
    assert database_name == test_database_settings.database_name
    return database_name
