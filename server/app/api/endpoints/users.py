from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from supabase import Client

from app.api import deps
from app.schemas import user as user_schema
from app.crud import crud_user

router = APIRouter()

@router.get("/me", response_model=user_schema.User)
def read_users_me(current_user: Dict[str, Any] = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """
    return current_user

@router.get("/employees", response_model=List[user_schema.User])
def read_employees(db: Client = Depends(deps.get_db)):
    """
    Retrieve all employees who are not yet assigned to a team.
    """
    return crud_user.get_unassigned_employees(db)
