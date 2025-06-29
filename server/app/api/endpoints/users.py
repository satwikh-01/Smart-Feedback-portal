from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.api import deps
from app.schemas import user as user_schema

router = APIRouter()

@router.get("/me", response_model=user_schema.User)
def read_users_me(current_user: Dict[str, Any] = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """
    return current_user
