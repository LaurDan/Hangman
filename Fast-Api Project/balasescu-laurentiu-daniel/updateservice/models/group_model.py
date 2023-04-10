import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime,String
from updateservice.db_connection import Base

class Group(Base):
    __tablename__ = "group"

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
