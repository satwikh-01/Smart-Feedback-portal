from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Role

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    team_id: Optional[int] = None

class User(UserBase):
    id: int
    team_id: Optional[int] = None

    class Config:
        from_attributes = True