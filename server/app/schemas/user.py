import enum
from pydantic import BaseModel, EmailStr
from typing import Optional

# Moved the Role Enum from the old models file to here
class Role(str, enum.Enum):
    manager = "manager"
    employee = "employee"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Role

class UserCreate(UserBase):
    password: str
    # Add team_name for manager registration and team_id for employee registration
    team_name: Optional[str] = None
    team_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    team_id: Optional[int] = None

class User(UserBase):
    id: int
    team_id: Optional[int] = None

    class Config:
        # Pydantic v2 uses `from_attributes` instead of `orm_mode`
        from_attributes = True
