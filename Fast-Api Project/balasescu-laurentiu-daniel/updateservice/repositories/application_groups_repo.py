import uuid
from sqlalchemy import select, delete
from updateservice.db_connection import async_session
from ..models.application_groups_model import ApplicationGroups

class AppAssignedNotFoundException(Exception):
    pass

class ApplicationGroupsRepo:

    async def create_application_groups(self, app_id: int, group_id: str):
        async with async_session() as session:
            new_app_groups = ApplicationGroups(id=str(uuid.uuid4()), application_id=app_id, group_id=group_id)
            session.add(new_app_groups)
            await session.commit()
            return "Application successfully assigned to the group"

    async def unassign_app_from_group(self, app_id: int, group_id: str):
        async with async_session() as session:
            pack_query = await session.execute(
                select(ApplicationGroups).filter(
                    ApplicationGroups.application_id == app_id, ApplicationGroups.group_id == group_id
                )
            )
            pack_check_query = pack_query.first()
            if pack_check_query is None:
                raise AppAssignedNotFoundException("Application has been already unassigned from group!")
            unassign_app = (
                delete(ApplicationGroups)
                .where(ApplicationGroups.application_id == app_id)
                .where(ApplicationGroups.group_id == group_id)
            )
            await session.execute(unassign_app)
            await session.commit()
            return "Application successfully unassigned from the group"
