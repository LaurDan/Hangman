from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from..repositories.application_groups_repo import AppAssignedNotFoundException
from ..repositories.groups_repo import GroupIdNotFoundException
from ..services.application_group_srv import ApplicationGroupsService
from ..services.groups_srv import GroupService
from ..services.application_service import AppService

router = APIRouter(tags=["Application Groups"])


@router.post("/v1/applications/{app_id}/groups/{group_id}")
async def assign_application_to_group(
        app_id: int,
        group_id: str,
        app_srv: AppService = Depends(AppService),
        group_srv: GroupService = Depends(GroupService),
        app_group_srv: ApplicationGroupsService = Depends(ApplicationGroupsService)
):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Application Id not found in the system"
        )
    try:
        await group_srv.fetch_one_group_srv(group_id)
    except GroupIdNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error)
        )

    result = await app_group_srv.assign_application_to_group_srv(app_id, group_id)
    return result

@router.delete("/v1/applications/{app_id}/groups/{group_id}")
async def unassign_application_from_group(
        app_id: int,
        group_id: str,
        app_srv: AppService = Depends(AppService),
        group_srv: GroupService = Depends(GroupService),
        app_group_srv: ApplicationGroupsService = Depends(ApplicationGroupsService)
):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Application Id not found in the system"
        )
    try:
        await group_srv.fetch_one_group_srv(group_id)
    except GroupIdNotFoundException as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error)
        )
    try:
        result = await app_group_srv.unassign_application_from_group_srv(app_id, group_id)
    except AppAssignedNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return result
