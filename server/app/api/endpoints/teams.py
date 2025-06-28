from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client # Replaced Session with Client
from typing import List, Dict, Any

from app.crud import crud_team, crud_user
from app.schemas import team as team_schema
from app.schemas import user as user_schema
from app.api import deps

# The import for the SQLAlchemy UserModel is no longer needed.
# from app.models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=team_schema.Team, status_code=status.HTTP_201_CREATED)
def create_team(
    *,
    db: Client = Depends(deps.get_db),
    team_in: team_schema.TeamCreate,
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Create a new team. Only accessible to managers.
    A manager can only create one team.
    """
    existing_team = crud_team.get_team_by_manager(db, manager_id=current_user['id'])
    if existing_team:
        raise HTTPException(
            status_code=400,
            detail="Manager already has a team.",
        )
    team = crud_team.create_team(db=db, team_in=team_in, manager_id=current_user['id'])
    return team

@router.get("/me", response_model=team_schema.Team)
def read_my_team(
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Get the current manager's team details.
    """
    team = crud_team.get_team_by_manager(db, manager_id=current_user['id'])
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/{team_id}/members/{user_id}", response_model=user_schema.User)
def add_team_member(
    team_id: int,
    user_id: int,
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Add an employee to a team.
    """
    team = crud_team.get_team_by_manager(db, manager_id=current_user['id'])
    if not team or team['id'] != team_id:
        raise HTTPException(
            status_code=403, detail="Cannot add members to another manager's team"
        )

    user_to_add = crud_user.get_user(db, user_id=user_id)
    if not user_to_add:
        raise HTTPException(status_code=404, detail="Employee not found")
    if user_to_add['role'] != "employee":
        raise HTTPException(status_code=400, detail="Can only add users with the 'employee' role")
    if user_to_add.get('team_id'):
        raise HTTPException(status_code=400, detail="Employee is already in a team")

    # We will modify crud_team.add_employee_to_team later
    return crud_team.add_employee_to_team(db=db, team_id=team['id'], user_id=user_to_add['id'])