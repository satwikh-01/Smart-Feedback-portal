from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from typing import List, Dict, Any

from app.crud import crud_team, crud_user, crud_feedback # Import crud_feedback
from app.schemas import team as team_schema
from app.schemas import user as user_schema
from app.api import deps

router = APIRouter()

@router.post("/", response_model=team_schema.Team, status_code=status.HTTP_201_CREATED)
def create_team(
    *,
    db: Client = Depends(deps.get_db),
    team_in: team_schema.TeamCreate,
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
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

    return crud_team.add_employee_to_team(db=db, team_id=team['id'], user_id=user_to_add['id'])


@router.get("/me/stats", response_model=List[Dict[str, Any]])
def get_my_team_stats(
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Get aggregated feedback statistics for the current manager's team.
    """
    stats = crud_feedback.get_feedback_stats_by_manager(db, manager_id=current_user['id'])
    return stats

@router.get("/", response_model=List[team_schema.TeamPublic])
def read_teams(db: Client = Depends(deps.get_db)):
    """
    Retrieve all teams. This is a public endpoint.
    """
    teams = crud_team.get_all_teams(db)
    return teams
