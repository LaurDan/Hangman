from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from updateservice.db_connection import Base


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, unique=True)
    tokens = Column(String(255), unique=True)
    deleted = Column(Boolean(False))
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow())
    updated_at = Column(
        TIMESTAMP, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    user = relationship("User", backref=backref("token"))
