import pytest

from updateservice.repositories.healthcheck_repo import ABCHealthcheckRepo
from updateservice.services.healthcheck_service import HealthcheckService


@pytest.mark.asyncio
async def test_health_service_db_unavailable():
    class TestHealthcheckRepository(ABCHealthcheckRepo):
        async def healthcheck_repo_api(self):
            raise Exception

    service = HealthcheckService(repo=TestHealthcheckRepository())
    result = await service.healthcheck_service_api()

    assert result == "Database is unavailable"


@pytest.mark.asyncio
async def test_health_service_db_available():
    class TestHealthcheckRepository(ABCHealthcheckRepo):
        async def healthcheck_repo_api(self):
            pass

    service = HealthcheckService(repo=TestHealthcheckRepository())
    result = await service.healthcheck_service_api()

    assert result == "Database is available"
