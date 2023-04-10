from fastapi import HTTPException, status
from sqlalchemy import update, or_, and_
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from updateservice.db_connection import async_session
from updateservice.models.application_groups_model import ApplicationGroups
from updateservice.models.application_model import Application
from updateservice.models.schemas.app_schema import (
    ApplicationCreate,
    ApplicationUpdate, ApplicationGroupBase
)
from updateservice.models.user_teams import Team


class AppRepo:
    async def create_app(self, team_id: int, app: ApplicationCreate):
        async with async_session() as session:
            query = await session.execute(select(Team).filter(Team.id == team_id))
            app_to_create = query.first()
            if app_to_create is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The team with this id does not exist in the system",
                )
            db_app = Application(
                team_id=team_id, name=app.name, description=app.description
            )
            db_app.team_ = app_to_create[0]
            session.add(db_app)
            await session.commit()
            await session.refresh(db_app)
            return db_app

    async def get_all_apps(self, team_id: int, page: int = 1, page_size: int = 20, search_query: str = None):
        async with async_session() as session:
            query = await session.execute(select(Team).filter(Team.id == team_id))
            team_query = query.first()
            if team_query is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The team with this id does not exist in the system",
                )
            offset = (page - 1) * page_size
            limit = page_size
            query_app = (
                select(Application)
                .filter(Application.team_id == team_id)
                .order_by(Application.id)
                .offset(offset)
                .limit(limit)
            )
            if search_query:
                query_app = query_app.filter(
                    or_(
                        Application.name.ilike(f"%{search_query}%"),
                        Application.description.ilike(f"%{search_query}%"),
                    )
                )
            query_result = await session.execute(query_app)
            app = [
                {"name": a.name, "description": a.description, "team_": {"id": team_id}}
                for a in query_result.scalars().all()
            ]
            return app

    async def update_app(self, app_id: int, app: ApplicationUpdate):
        async with async_session() as session:
            app_query = await session.execute(
                select(Application).filter(Application.id == app_id)
            )
            app_to_update = app_query.first()
            if app_to_update is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The application with this id does not exist in the system",
                )
            update_app = (
                update(Application)
                .where(Application.id == app_id)
                .values(name=app.name, description=app.description)
            )
            await session.execute(update_app)
            await session.commit()

            result = await session.execute(
                select(
                    Application.id, Application.name, Application.description
                ).filter(Application.id == app_id)
            )
            return result

    async def fetch_one_app(self, app_id: int):
        async with async_session() as session:
            app_query = await session.execute(
                select(Application).filter((Application.id == app_id))
            )
            app = app_query.scalar_one()
            return app

    async def fetch_one_app_for_groups(self, team_id: int, app_id: int):
        async with async_session() as session:
            gr_query = await session.execute(select(ApplicationGroups.group_id)
                                             .filter(ApplicationGroups.application_id == app_id))
            group_res = gr_query.scalars().all()
            group_ids = [str(g) for g in group_res]
            app_query = (
                select(Application)
                .options(joinedload(Application.team))
                .where(and_(Application.id == app_id, Application.team_id == team_id))
            )
            app_result = await session.execute(app_query)
            result = app_result.scalar_one()
            result_dict = result.to_dict()
            result_dict['groups'] = group_ids

            return ApplicationGroupBase(**result_dict)
