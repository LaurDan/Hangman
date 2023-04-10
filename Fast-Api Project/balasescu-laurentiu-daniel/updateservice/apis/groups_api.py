from fastapi import APIRouter, Depends, HTTPException, status
from ..repositories.groups_repo import UniqueNameException, GroupIdNotFoundException
from ..services.groups_srv import GroupService
from ..models.schemas.groups_schema import GroupBase, GroupCreate
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["Groups"])

@router.post("/v1/groups/", response_model=GroupBase)
async def create_application_group(group: GroupCreate, group_srv: GroupService = Depends(GroupService)):
    try:
        return await group_srv.create_group_srv(group)
    except UniqueNameException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

@router.delete("/v1/groups/{group_id}")
async def delete_group(group_id: str, group_srv: GroupService = Depends(GroupService)):
    try:
        await group_srv.fetch_one_group_srv(group_id)
    except GroupIdNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    try:
        result = await group_srv.delete_group_srv(group_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete!Applications assigned to the group!"
        )

    return result
