from fastapi import Depends
from ..repositories.app_repo import AppRepo
from asyncpg.exceptions import UniqueViolationError

class AppService:
    def __init__(self, repo: AppRepo = Depends(AppRepo)):
        self.repo = repo

    async def fetch_one_app(self, app_id: int):
        try:
            await self.repo.fetch_one_app(app_id)
        except ValueError:
            raise UniqueViolationError

    async def get_all_apps_srv(
        self, team_id: int, page: int = 1, page_size: int = 20, search_query: str = None
    ):
        try:
            result = await self.repo.get_all_apps(team_id, page, page_size, search_query)
        except ValueError:
            raise UniqueViolationError
        return result

    async def fetch_one_app_for_group_srv(
        self, team_id: int, app_id: int
    ):
        try:
            result = await self.repo.fetch_one_app_for_groups(team_id, app_id)
        except ValueError:
            raise UniqueViolationError
        return result
