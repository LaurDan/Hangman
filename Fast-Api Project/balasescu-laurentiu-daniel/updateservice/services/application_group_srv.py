from fastapi import Depends
from ..repositories.application_groups_repo import ApplicationGroupsRepo


class ApplicationGroupsService:
    def __init__(self, repo: ApplicationGroupsRepo = Depends(ApplicationGroupsRepo)):
        self.repo = repo

    async def assign_application_to_group_srv(self, app_id: int, group_id: str):
        try:
            result = await self.repo.create_application_groups(app_id, group_id)
        except ValueError:
            raise ValueError
        return result

    async def unassign_application_from_group_srv(self, app_id: int, group_id: str):
        try:
            result = await self.repo.unassign_app_from_group(app_id, group_id)
        except ValueError:
            raise ValueError
        return result
