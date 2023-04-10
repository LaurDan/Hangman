import pytest
from fastapi import HTTPException

from updateservice.apis.api_healthcheck import healthcheck_api
from updateservice.services.healthcheck_service import ABCHealthcheckService


@pytest.mark.asyncio
async def test_health_check_api_db_is_available():
    class TestHealthcheckService(ABCHealthcheckService):
        async def healthcheck_service_api(self):
            return "Database is available"

    response = await healthcheck_api(health_check=TestHealthcheckService())
    assert response == {"detail": "Application is healthy!"}


@pytest.mark.asyncio
async def test_health_check_api_db_is_not_available():
    class TestHealthcheckService(ABCHealthcheckService):
        async def healthcheck_service_api(self):
            return "Database is unavailable"

    with pytest.raises(HTTPException) as e:
        await healthcheck_api(health_check=TestHealthcheckService())
    assert e.value.detail == "Application is not healthy! Database is unavailable"
