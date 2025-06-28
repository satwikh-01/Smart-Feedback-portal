from typing import List, Dict, Any, Optional
from supabase import Client
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

# Note: We no longer need imports from sqlalchemy.orm or app.models

def create_feedback(db: Client, *, feedback_in: FeedbackCreate, manager_id: int) -> Optional[Dict[str, Any]]:
    """
    Creates a new feedback entry in the database using Supabase.
    """
    feedback_data = feedback_in.model_dump()
    feedback_data['manager_id'] = manager_id
    
    response = db.table("feedback").insert(feedback_data).execute()
    
    if not response.data:
        return None
        
    return response.data[0]

def get_feedback_by_employee(db: Client, *, employee_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all feedback for a specific employee from Supabase, including related data
    for PDF generation.
    """
    response = db.table("feedback").select(
        "*, manager:users!feedback_manager_id_fkey(*), comments(*, user:users(*))"
    ).eq("employee_id", employee_id).execute()
    return response.data if response.data else []

def get_feedback_by_manager(db: Client, *, manager_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all feedback submitted by a specific manager from Supabase, including related data
    for PDF generation.
    """
    response = db.table("feedback").select(
        "*, employee:users!feedback_employee_id_fkey(*), comments(*, user:users(*))"
    ).eq("manager_id", manager_id).execute()
    return response.data if response.data else []

def get_feedback(db: Client, *, feedback_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves a single piece of feedback by its ID from Supabase.
    """
    response = db.table("feedback").select("*").eq("id", feedback_id).single().execute()
    return response.data if response.data else None

def update_feedback(db: Client, *, db_obj: Dict[str, Any], obj_in: FeedbackUpdate) -> Optional[Dict[str, Any]]:
    """
    Updates a feedback entry in Supabase.
    """
    update_data = obj_in.model_dump(exclude_unset=True)
    if not update_data:
        return db_obj # Return original object if there's nothing to update
        
    response = db.table("feedback").update(update_data).eq("id", db_obj['id']).execute()
    
    if not response.data:
        return None
        
    return response.data[0]

def acknowledge_feedback(db: Client, *, db_obj: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Marks a feedback entry as acknowledged by the employee in Supabase.
    """
    response = db.table("feedback").update({"acknowledged": True}).eq("id", db_obj['id']).execute()

    if not response.data:
        return None
        
    return response.data[0]