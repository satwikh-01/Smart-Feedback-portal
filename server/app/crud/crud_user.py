from typing import Optional, Dict, Any, List
from supabase import Client
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.crud import crud_team

def get_user_by_email(db: Client, *, email: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a user from the database by their email address.
    """
    response = db.table("users").select("*").eq("email", email).execute()
    if response.data:
        return response.data[0]
    return None

def get_user(db: Client, *, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a user from the database by their ID.
    """
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return None
    response = db.table("users").select("*").eq("id", user_id_int).single().execute()
    return response.data if response.data else None

def get_unassigned_employees(db: Client) -> List[Dict[str, Any]]:
    """
    Fetches all employees who are not yet assigned to a team.
    """
    response = db.table("users").select("*").eq("role", "employee").is_("team_id", "null").execute()
    return response.data if response.data else []

def create_user_with_team(db: Client, *, user_in: UserCreate) -> Optional[Dict[str, Any]]:
    """
    Creates a new user.
    - If the user is a manager, it also creates a new team for them.
    - If the user is an employee, it assigns them to an existing team.
    """
    # 1. Prepare base user data
    hashed_password = get_password_hash(user_in.password)
    user_data = {
        "email": user_in.email,
        "full_name": user_in.full_name,
        "role": user_in.role.value,
        "hashed_password": hashed_password,
        "team_id": user_in.team_id, # Will be null for managers initially
    }

    # 2. Handle manager creation
    if user_in.role.value == 'manager':
        if not user_in.team_name:
            # A team name is required for managers
            raise ValueError("Manager registration requires a team name.")
        
        # A manager is not initially assigned a team_id
        user_data["team_id"] = None
        
        # Create the manager user first
        user_response = db.table("users").insert(user_data).execute()
        if not user_response.data:
            raise Exception("Failed to create manager user.")
        
        new_manager = user_response.data[0]
        manager_id = new_manager['id']
        
        # Create a new team with the manager's ID
        new_team = crud_team.create_team(db, name=user_in.team_name, manager_id=manager_id)
        if not new_team:
            # Rollback or handle team creation failure
            db.table("users").delete().eq("id", manager_id).execute()
            raise Exception("Failed to create team for manager.")
        
        # Update the manager with their new team_id
        updated_user_response = db.table("users").update({"team_id": new_team['id']}).eq("id", manager_id).execute()
        if not updated_user_response.data:
            # Handle the unlikely event of the update failing
            raise Exception("Failed to assign team to manager.")
            
        return updated_user_response.data[0]

    # 3. Handle employee creation
    elif user_in.role.value == 'employee':
        if user_in.team_id is None:
            # An employee must be assigned to a team
            raise ValueError("Employee registration requires a team_id.")
        
        user_response = db.table("users").insert(user_data).execute()
        if not user_response.data:
            raise Exception("Failed to create employee user.")
            
        return user_response.data[0]
    
    else:
        # Handle any other role or invalid input
        raise ValueError("Invalid user role specified.")
