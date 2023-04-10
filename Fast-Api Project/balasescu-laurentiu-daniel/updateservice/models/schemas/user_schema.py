from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserSearchQueryParams(BaseModel):
    search: Optional[str] = None

class UserBase(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):

    email: str
    full_name: Optional[str]

    class Config:
        orm_mode = True
