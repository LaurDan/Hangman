from datetime import datetime

from sqlalchemy import (TIMESTAMP, VARCHAR, CheckConstraint, Column,
                        ForeignKey, Integer)
from sqlalchemy.orm import backref, relationship

from updateservice.db_connection import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(255), unique=True)
    full_name = Column(VARCHAR(255), unique=True)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow())
    updated_at = Column(
        TIMESTAMP, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), CheckConstraint("name != ''"), unique=True)
    description = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow())
    updated_at = Column(
        TIMESTAMP, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class UserTeams(Base):
    __tablename__ = "team_users_table"

    id = Column(Integer, primary_key=True)

    team_id = Column(Integer, ForeignKey("team.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(
        TIMESTAMP,
        default=datetime.now(),
        onupdate=datetime.now(),
    )
    user = relationship("User", backref=backref("team_users_table"))
    team = relationship("Team", backref=backref("team_users_table"))
