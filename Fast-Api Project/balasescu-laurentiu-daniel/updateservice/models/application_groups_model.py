import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from updateservice.db_connection import Base
from ..models.group_model import Group
from ..models.application_model import Application


class ApplicationGroups(Base):
    __tablename__ = "application_groups"

    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4())
    )
    application_id = Column(Integer, ForeignKey("application.id"))
    application = relationship("Application", backref=backref("application_groups"))

    group_id = Column(String, ForeignKey("group.id"))
    group = relationship("Group", backref=backref("application_groups"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
