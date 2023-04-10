from typing import Any, Dict, Optional

from pydantic import BaseModel


class TokenBase(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    token: Optional[str]
    deleted: Optional[bool]

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        orm_mode = True


class TokenCreate(BaseModel):

    id: Optional[int]
    user_id: Optional[int]
    token: str

    class Config:
        orm_mode = True


class TokenSettings(BaseModel):
    id: Optional[int]
    deleted: Optional[bool]

    class Config:
        orm_mode = True


class TokenWithId(BaseModel):
    id: int
    user_id: int
    token: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: Optional[str] = None
