from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class GroupBase(BaseModel):
    id: str
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class GroupCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True
