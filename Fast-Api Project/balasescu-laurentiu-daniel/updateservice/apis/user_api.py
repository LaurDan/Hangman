from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from updateservice.models.schemas.user_schema import UserBase, UserCreate
from ..services.user_srv import UserService
from updateservice.repositories.user_repo import UserRepo

router = APIRouter(tags=["user"])


@router.post(
    "/internal/v1/users", response_model=UserBase, status_code=status.HTTP_201_CREATED
)
async def create_new_user(user: UserCreate, db: UserRepo = Depends(UserRepo)):
    try:
        new_user = await db.create_user(user)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="User name already registered"
        )
    return new_user

@router.get("/internal/v1/users", response_model=List[UserBase])
async def list_all_users(
    search: Optional[str] = None,
    user_srv: UserService = Depends(UserService)
):
    if search:
        users = await user_srv.search_users_srv(search)
    else:
        users = await user_srv.get_all_users_srv()

    return users
