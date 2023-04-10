from ..repositories.groups_repo import GroupRepo
from asyncpg.exceptions import UniqueViolationError
from fastapi import Depends
from ..models.schemas.groups_schema import GroupCreate


class GroupService:
    def __init__(self, repo: GroupRepo = Depends(GroupRepo)):
        self.repo = repo

    async def create_group_srv(self, group: GroupCreate):
        try:
            result = await self.repo.create_group(group)
        except ValueError:
            raise UniqueViolationError
        return result

    async def fetch_one_group_srv(self, group_id: str):
        try:
            result = await self.repo.fetch_one_group(group_id)
        except ValueError:
            raise UniqueViolationError
        return result

    async def delete_group_srv(self, group_id: str):
        try:
            result = await self.repo.delete_group(group_id)
        except ValueError:
            raise UniqueViolationError
        return result
