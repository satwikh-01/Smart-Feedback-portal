import enum
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
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