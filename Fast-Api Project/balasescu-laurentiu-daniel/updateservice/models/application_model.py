from sqlalchemy import VARCHAR, CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from updateservice.db_connection import Base


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), CheckConstraint("name != ''"), unique=True)
    description = Column(VARCHAR(255))

    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("Team", backref=backref("application"))

    group_id = Column(String, ForeignKey("group.id"))
    groups = relationship("Group", backref="application")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'team': self.team_id,
            'group_id': self.group_id
        }
