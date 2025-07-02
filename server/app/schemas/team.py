from pydantic import BaseModel
from typing import List, Optional
from .user import User

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    manager: User
    members: List[User] = []

    class Config:
        from_attributes = True

class TeamPublic(BaseModel):
    id: int
    name: str
