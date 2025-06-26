from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # The manager of the team
    manager = relationship("User", back_populates="managed_team", foreign_keys=[manager_id])

    # The members of the team
    members = relationship("User", back_populates="team", foreign_keys="[User.team_id]")