from ..repositories.team_repo import TeamRepo
from fastapi import Depends
from asyncpg.exceptions import UniqueViolationError

class TeamService:
    def __init__(self, repo: TeamRepo = Depends(TeamRepo)):
        self.repo = repo

    async def get_all_teams_srv(self, page: int = 1, page_size: int = 20):
        try:
            result = await self.repo.get_all_teams(page, page_size)
        except ValueError:
            raise UniqueViolationError
        return result

    async def fetch_one_srv(self, team_id: int):
        try:
            result = await self.repo.fetch_one(team_id)
        except ValueError:
            raise UniqueViolationError
        return result
