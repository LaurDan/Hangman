import pytest

from updateservice.db_connection import async_session


@pytest.mark.asyncio
async def test_db_conn():
    async with async_session() as session:
        cursor = await session.execute("select 100 as dummy")
        result = cursor.fetchall()
    assert len(result) == 1
    assert result[0].dummy == 100
