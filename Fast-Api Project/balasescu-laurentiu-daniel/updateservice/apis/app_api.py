from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..services.application_service import AppService
from updateservice.models.schemas.app_schema import (
ApplicationBase,
ApplicationCreate,
ApplicationUpdate,
ApplicationGroupBase
)
from updateservice.repositories.app_repo import AppRepo
from updateservice.repositories.team_repo import TeamRepo
from ..services.team_service import TeamService

router = APIRouter(tags=["application"])


@router.post(
    "/v1/teams/{team_id}/applications/",
    response_model=ApplicationBase,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_app_for_team_with_token_access(
    team_id: int, app: ApplicationCreate, db: AppRepo = Depends(AppRepo)
):
    try:
        new_item = await db.create_app(team_id, app)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="Team name already exists in the system"
        )
    return new_item


@router.get(
    "/v1/teams/{team_id}/applications",
    response_model=List[ApplicationBase],
    status_code=status.HTTP_200_OK,
)
async def list_all_applications_of_a_team(
    team_id: int,
    page: int = 1,
    page_size: int = 20,
    search_query: Optional[str] = None,
    repo: AppService = Depends(AppService),
):
    list_items = await repo.get_all_apps_srv(team_id, page, page_size, search_query)
    return list_items


@router.patch(
    "/v1/teams/{team_id}/applications/{app_id}", response_model=ApplicationBase
)
async def update_app(
    team_id: int,
    app_id: int,
    app: ApplicationUpdate,
    db: TeamRepo = Depends(TeamRepo),
    repo: AppRepo = Depends(AppRepo),
):
    try:
        fetch_one = await db.fetch_one(team_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Team Id not found in the system"
        )
    try:
        await repo.update_app(app_id, app)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Application already registered in the system",
        )
    result = ApplicationBase(
        name=app.name, description=app.description, team_=fetch_one
    )
    return result


@router.get(
    "/v1/teams/{team_id}/applications/{app_id}", response_model=ApplicationGroupBase
)
async def get_application_details(
    team_id: int,
    app_id: int,
    team_srv: TeamService = Depends(TeamService),
    api_srv: AppService = Depends(AppService),
):
    try:
        await team_srv.fetch_one_srv(team_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Team with this id does not exists in the system",
        )
    try:
        res = await api_srv.fetch_one_app_for_group_srv(team_id, app_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Application with this id does not exists in the system",
        )
    return res
