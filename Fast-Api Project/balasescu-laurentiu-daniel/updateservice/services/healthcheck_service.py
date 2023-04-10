import abc

from fastapi import Depends

from ..repositories.healthcheck_repo import (
    ABCHealthcheckRepo,
    HealthcheckRepository
)


class ABCHealthcheckService:
    @abc.abstractmethod
    async def healthcheck_service_api(self):
        pass


class HealthcheckService(ABCHealthcheckService):
    def __init__(self, repo: ABCHealthcheckRepo = Depends(HealthcheckRepository)):
        self.repo = repo

    async def healthcheck_service_api(self):
        try:
            await self.repo.healthcheck_repo_api()
            return "Database is available"
        except Exception as e:
            return "Database is unavailable"
