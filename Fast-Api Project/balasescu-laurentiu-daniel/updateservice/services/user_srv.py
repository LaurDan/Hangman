from asyncpg import UniqueViolationError

from ..repositories.user_repo import UserRepo
from fastapi import Depends


class UserService:
    def __init__(self, repo: UserRepo = Depends(UserRepo)):
        self.repo = repo

    async def search_users_srv(self, search: str):
        try:
            result = await self.repo.search_users(search)
        except ValueError:
            raise UniqueViolationError
        return result

    async def get_all_users_srv(self):
        try:
            result = await self.repo.get_all_users()
        except ValueError:
            raise UniqueViolationError
        return result
