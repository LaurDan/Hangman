import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from ..models.group_model import Group
from ..db_connection import async_session
from ..models.schemas.groups_schema import GroupCreate


class GroupIdNotFoundException(Exception):
    pass

class UniqueNameException(Exception):
    pass


class GroupRepo:
    async def create_group(self, group: GroupCreate):
        async with async_session() as session:
            new_group = Group(id=str(uuid.uuid4()), name=group.name)
            session.add(new_group)
            try:
                await session.commit()
                return new_group
            except IntegrityError:
                raise UniqueNameException("A group with this name already exists in the system!")


    async def fetch_one_group(self, group_id: str):
        async with async_session() as session:
            query = await session.execute(select(Group).filter(Group.id == group_id))
            result = query.first()
            if result is None:
                raise GroupIdNotFoundException(f"Group with id {group_id} not found in the system!")
            return result

    async def delete_group(self, group_id: str):
        async with async_session() as session:
            delete_query = (
                delete(Group).where(Group.id == group_id)
            )
            await session.execute(delete_query)
            await session.commit()
            return "Group has been deleted"
