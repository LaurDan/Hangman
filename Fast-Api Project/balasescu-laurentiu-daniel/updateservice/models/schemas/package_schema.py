from typing import Optional

from pydantic import BaseModel


class ApplicationId(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True


class PackageBase(BaseModel):
    id: str
    version: str
    description: str
    file_name: Optional[str]
    hash: Optional[str]
    size: Optional[int]
    file_path: Optional[str]
    appl: ApplicationId

    class Config:
        orm_mode = True


class PackageCreate(BaseModel):

    version: str
    description: str

    class Config:
        schema_extra = {"example": {"version": "x.y.z", "description": "string"}}
        orm_mode = True

class PackageUpdate(BaseModel):
    id: str
    version: str
    description: str
    file_name: Optional[str]
    hash: Optional[str]
    file_path: Optional[str]
    size: Optional[int]
    appl: ApplicationId

    class Config:
        orm_mode = True

class Packages(BaseModel):
    id: str
    version: str
    description: str

    class Config:
        orm_mode = True
