from typing import List
from ..services.team_service import TeamService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from updateservice.models.schemas.team_schema import (TeamBase, TeamCreate,
                                                      TeamUpdate)
from updateservice.repositories.team_repo import TeamRepo

router = APIRouter(prefix="/internal/v1/teams", tags=["teams"])


@router.get("/{team_id}", response_model=TeamBase, status_code=status.HTTP_200_OK)
async def get_object_or_404(team_id: int, db: TeamRepo = Depends(TeamRepo)):
    try:
        db_user = await db.fetch_one(team_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Id not found in the system"
        )
    return db_user


@router.get("/", response_model=List[TeamBase], status_code=status.HTTP_200_OK)
async def get_teams(page: int = 1, page_size: int = 20, db: TeamService = Depends(TeamService)):
    teams = await db.get_all_teams_srv(page=page, page_size=page_size)
    results = [team for team in teams]
    return results


@router.post("/", response_model=TeamBase, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamCreate, db: TeamRepo = Depends(TeamRepo)):
    try:
        new_item = await db.create_team(team)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already registered in the system",
        )
    return new_item


@router.put("/{team_id}", response_model=TeamBase, status_code=status.HTTP_200_OK)
async def update_team(team_id: int, team: TeamUpdate, db: TeamRepo = Depends(TeamRepo)):
    try:
        updated_item = await db.update_team(team_id, team)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team with this name already exits in the system",
        )
    return updated_item
