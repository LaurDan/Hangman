from typing import Optional, List

from pydantic import BaseModel


class Team(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    name: str
    description: Optional[str] | None = None
    team_: Team

    class Config:
        orm_mode = True


class ApplicationCreate(BaseModel):

    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class ApplicationUpdate(BaseModel):
    name: str
    description: Optional[str] | None = None

    class Config:
        orm_mode = True


class ApplicationDetails(BaseModel):

    name: str
    description: Optional[str]
    team_: Team

    class Config:
        orm_mode = True

class GroupsId(BaseModel):
    id: Optional[str]

    class Config:
        orm_mode = True

class ApplicationGroupBase(BaseModel):
    id: int
    name: str
    description: Optional[str] | None = None
    team: int
    groups: List[str] = []
    class Config:
        orm_mode = True
