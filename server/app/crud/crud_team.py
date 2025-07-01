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
    Fetches the team managed by a specific manager using a single query with joins.
    """
    # Use Supabase's foreign key embedding to fetch related data
    # This assumes you have foreign key relationships set up in your Supabase tables:
    # - `teams.manager_id` references `users.id`
    # - `users.team_id` references `teams.id`
    response = (
        db.table("teams")
        .select("*, manager:users!manager_id(*), members:users!team_id(*)")
        .eq("manager_id", manager_id)
        .single()
        .execute()
    )
    
    return response.data if response.data else None

def get_all_teams(db: Client) -> list[Dict[str, Any]]:
    """
    Fetches all teams from Supabase.
    """
    response = db.table("teams").select("id, name").execute()
    return response.data if response.data else []


def create_team(db: Client, *, name: str, manager_id: int) -> Optional[Dict[str, Any]]:
    """
    Creates a new team for a manager in Supabase.
    """
    team_data = {"name": name, "manager_id": manager_id}
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
