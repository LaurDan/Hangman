from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TeamBase(BaseModel):
    id: Optional[int]
    name: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class TeamCreate(BaseModel):

    name: str
    description: str

    class Config:
        orm_mode = True


class TeamUpdate(BaseModel):

    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: Optional[str]
    full_name: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: Optional[str]
    full_name: Optional[str]

    class Config:
        orm_mode = True


class UserSchema(UserBase):
    team: List[TeamBase]


class TeamSchema(TeamBase):
    user: List[UserBase]
