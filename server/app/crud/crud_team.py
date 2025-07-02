from typing import Optional, Dict, Any
from supabase import Client
from app.schemas.team import TeamCreate

def get_team(db: Client, *, team_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetches a team by its ID from Supabase.
    """
    response = db.table("teams").select("*").eq("id", team_id).single().execute()
    return response.data if response.data else None

def get_team_by_manager(db: Client, *, manager_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetches the team managed by a specific manager.
    This version uses two separate queries for robustness.
    """
    # Step 1: Fetch the team for the manager
    team_response = db.table("teams").select("*").eq("manager_id", manager_id).single().execute()
    
    if not team_response.data:
        return None
    
    team = team_response.data
    
    # Step 2: Fetch the members of that team
    members_response = db.table("users").select("*").eq("team_id", team['id']).execute()
    
    # Step 3: Combine the results
    team['members'] = members_response.data if members_response.data else []
    
    # The manager details are already part of the user object, so we don't need a separate query for it.
    # We can assume the calling function will handle fetching the manager's user object if needed.
    team['manager'] = {} # Placeholder, as the full manager object isn't strictly needed here.

    return team

def get_all_teams(db: Client) -> list[Dict[str, Any]]:
    """
    Fetches all teams from Supabase.
    """
    response = db.table("teams").select("id, name").execute()
    return response.data if response.data else []


def create_team(db: Client, *, team_in: TeamCreate, manager_id: int) -> Optional[Dict[str, Any]]:
    """
    Creates a new team for a manager in Supabase.
    """
    team_data = team_in.model_dump()
    team_data["manager_id"] = manager_id
    response = db.table("teams").insert(team_data).execute()

    if not response.data:
        return None
        
    return response.data[0]

def add_employee_to_team(db: Client, *, team_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Assigns an employee to a team by updating the user's team_id in Supabase.
    """
    response = db.table("users").update({"team_id": team_id}).eq("id", user_id).execute()
    
    if not response.data:
        return None
        
    return response.data[0]
