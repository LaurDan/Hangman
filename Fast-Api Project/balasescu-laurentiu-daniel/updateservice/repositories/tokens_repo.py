from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy import update
from sqlalchemy.future import select

from updateservice.db_connection import async_session
from updateservice.models.token_model import Token
from updateservice.settings import SECRET_KEY

secret_key = SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30.0


class TokenRepo:
    async def create_access_token(self, expires_delta: Union[timedelta, None] = None):
        async with async_session() as session:
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=15)
            to_encode = {"exp": expire}
            encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
            tokens = encoded_jwt
            created_token = Token(tokens=tokens)
            session.add(created_token)
            await session.commit()
            await session.refresh(created_token)
            return encoded_jwt

    async def get_token_id(self, token: str):
        async with async_session() as session:
            query = select(Token.id).where(Token.tokens == token)
            result = await session.execute(query)
            return result.scalar()

    async def get_token_id_or_404(self, token_id: int):
        async with async_session() as session:
            result = await session.execute(select(Token).filter(Token.id == token_id))
            return result.scalar_one()

    async def soft_delete_repo(self, token_id: int):
        async with async_session() as session:
            result = await session.execute(select(Token).filter(Token.id == token_id))
            token_soft_delete = result.first()
            if token_soft_delete is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The token with this id does not exist in the system",
                )
            else:
                token_soft_delete = (
                    update(Token).where(Token.id == token_id).values(deleted=True)
                )
                await session.execute(token_soft_delete)
                await session.commit()
