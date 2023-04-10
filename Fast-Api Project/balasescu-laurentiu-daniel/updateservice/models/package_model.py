import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from updateservice.db_connection import Base


class Package(Base):
    __tablename__ = "package"

    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        nullable=False,
    )
    file_name = Column(String(255))
    version = Column(String, nullable=False)
    description = Column(String(255))
    hash = Column(String(64))
    size = Column(Integer)
    url = Column(String(1000))
    application_id = Column(Integer, ForeignKey("application.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    file_path = Column(String(255))
    appl = relationship(
        "Application", backref=backref("package", cascade="all, delete-orphan")
    )
