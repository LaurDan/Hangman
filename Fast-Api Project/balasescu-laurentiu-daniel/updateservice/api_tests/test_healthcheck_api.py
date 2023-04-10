from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@pytest.mark.asyncio
async def test_api_health(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"detail": "Application is healthy!"}


@pytest.mark.asyncio
async def test_healthcheck_api_for_bad_response(async_client):
    test_engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@0.0.0.0:5433/nonexistent_db",
        echo=True,
        future=True,
    )
    test_sessionmaker = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )
    with patch(
        "updateservice.repositories.healthcheck_repo.async_session",
        new=test_sessionmaker,
    ):
        result = await async_client.get("/health")
        assert result.status_code == 500
        assert result.json() == {
            "detail": "Application is not healthy! Database is unavailable"
        }
