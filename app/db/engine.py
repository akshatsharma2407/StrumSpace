from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings, TestDatabaseSettings, settings


DatabaseSettings = Settings | TestDatabaseSettings


def build_database_url(database_settings: DatabaseSettings = settings) -> URL:
    return URL.create(
        drivername="mysql+asyncmy",
        username=database_settings.database_user,
        password=database_settings.database_password.get_secret_value(),
        host=database_settings.database_host,
        port=database_settings.database_port,
        database=database_settings.database_name,
    )


def create_database_engine(database_settings: Settings = settings) -> AsyncEngine:
    return create_async_engine(
        build_database_url(database_settings),
        echo=database_settings.database_echo,
        pool_pre_ping=True,
        pool_size=database_settings.database_pool_size,
        max_overflow=database_settings.database_max_overflow,
        pool_timeout=database_settings.database_pool_timeout,
        pool_recycle=database_settings.database_pool_recycle,
    )


engine: AsyncEngine = create_database_engine()


async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def verify_database_connection() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def dispose_engine() -> None:
    await engine.dispose()
