from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.future import select

from updateservice.db_connection import async_session
from updateservice.models import user_teams
from updateservice.models.schemas.team_schema import TeamCreate, TeamUpdate
from updateservice.models.user_teams import Team


class TeamRepo:
    async def fetch_one(self, team_id: int):
        async with async_session() as session:
            result = await session.execute(select(Team).filter(Team.id == team_id))
            return result.scalar_one()

    async def get_all_teams(self, page: int = 1, page_size: int = 20):
        async with async_session() as session:
            offset = (page - 1) * page_size
            limit = page_size
            result = await session.execute(select(Team).order_by(Team.id).offset(offset).limit(limit))
            return result.scalars().all()

    async def create_team(self, team: TeamCreate):
        async with async_session() as session:
            db_user = Team(name=team.name, description=team.description)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user

    async def update_team(self, team_id: int, team: TeamUpdate):
        async with async_session() as session:
            query = await session.execute(select(Team).filter(Team.id == team_id))
            item_to_update = query.first()
            if item_to_update is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The team with this id does not exist in the system",
                )
            else:
                item_to_update = (
                    update(Team)
                    .where(user_teams.Team.id == team_id)
                    .values(team.dict(exclude_unset=True))
                )
                item_to_update.name = team.name
                item_to_update.description = team.description
                await session.execute(item_to_update)
                await session.commit()
                result = await session.execute(
                    select(
                        Team.id,
                        Team.name,
                        Team.description,
                        Team.created_at,
                        Team.updated_at,
                    ).filter(Team.id == team_id)
                )
                updated_team = result.first()
                return updated_team
