from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from updateservice.models.schemas.token_schema import TokenWithId
from updateservice.repositories.tokens_repo import (
    ACCESS_TOKEN_EXPIRE_MINUTES, TokenRepo)
from updateservice.repositories.user_repo import UserRepo

router = APIRouter(tags=["auth"])


@router.post(
    "/internal/v1/users/{user_id}/token",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenWithId,
)
async def generate_token(
    user_id: int,
    user_repo: UserRepo = Depends(UserRepo),
    token_repo: TokenRepo = Depends(TokenRepo),
):
    try:
        await user_repo.find_by_user_id(user_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    access_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = await token_repo.create_access_token(access_token)
    token_id = await token_repo.get_token_id(token)
    result = TokenWithId(id=token_id, user_id=user_id, token=token)
    return result


@router.delete(
    "/internal/v1/users/token/{token_id}", status_code=status.HTTP_201_CREATED
)
async def soft_delete_token(token_id: int, token_repo: TokenRepo = Depends(TokenRepo)):
    try:
        await token_repo.soft_delete_repo(token_id)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="Could not validate your request"
        )
    return "The token has been deleted"
