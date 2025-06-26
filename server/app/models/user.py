import enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Role(str, enum.Enum):
    manager = "manager"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(Role), nullable=False)

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    # A user who is a manager will have a team they manage
    managed_team = relationship("Team", back_populates="manager", foreign_keys="[Team.manager_id]")

    # A user who is an employee belongs to one team
    team = relationship("Team", back_populates="members", foreign_keys=[team_id])
