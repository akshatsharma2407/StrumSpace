from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_database_connection(db_session: AsyncSession, test_database_name: str) -> None:
    result = await db_session.execute(text("SELECT 1"))

    assert result.scalar_one() == 1
    assert test_database_name


async def test_database_session_rolls_back_uncommitted_work(
    db_session: AsyncSession,
) -> None:
    await db_session.execute(text("CREATE TEMPORARY TABLE task_1_8_session_test (value INT)"))
    await db_session.execute(text("INSERT INTO task_1_8_session_test (value) VALUES (1)"))
    await db_session.rollback()

    result = await db_session.execute(text("SELECT COUNT(*) FROM task_1_8_session_test"))
    assert result.scalar_one() == 0
