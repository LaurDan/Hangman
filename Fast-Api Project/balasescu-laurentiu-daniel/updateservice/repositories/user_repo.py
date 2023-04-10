from sqlalchemy.future import select
from sqlalchemy import or_
from updateservice.db_connection import async_session
from updateservice.models.schemas.user_schema import UserCreate
from updateservice.models.user_teams import User


class UserRepo:
    async def create_user(self, user: UserCreate):
        async with async_session() as session:
            db_user = User(email=user.email, full_name=user.full_name)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user

    async def find_by_user_id(self, user_id: int):
        async with async_session() as session:
            result = await session.execute(select(User).filter(User.id == user_id))
            return result.scalar_one()

    async def search_users(self, search: str):
        async with async_session() as session:
            query = select(User).filter(
                or_(
                    User.full_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%")
                )
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_all_users(self):
        async with async_session() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users
