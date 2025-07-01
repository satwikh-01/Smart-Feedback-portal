from typing import List, Dict, Any, Optional
from supabase import Client
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate


def create_feedback(db: Client, *, feedback_in: FeedbackCreate, manager_id: int) -> Optional[Dict[str, Any]]:
    """
    Creates a new feedback entry in the database using Supabase, with tags.
    """
    feedback_data = feedback_in.model_dump(exclude={"tag_ids"})
    feedback_data['manager_id'] = manager_id
    
    response = db.table("feedback").insert(feedback_data).execute()
    
    if not response.data:
        return None
        
    new_feedback = response.data[0]

    if feedback_in.tag_ids:
        feedback_tags_data = [
            {"feedback_id": new_feedback['id'], "tag_id": tag_id}
            for tag_id in feedback_in.tag_ids
        ]
        db.table("feedback_tags").insert(feedback_tags_data).execute()

    return new_feedback

def get_feedback_by_employee(db: Client, *, employee_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all feedback for a specific employee, including manager, comments with user details, and tags.
    """
    response = db.table("feedback").select(
        "*, manager:users!feedback_manager_id_fkey(*), employee:users!feedback_employee_id_fkey(*), tags(*)"
    ).eq("employee_id", employee_id).order("created_at", desc=True).execute()
    
    return response.data or []

def get_feedback_by_manager(db: Client, *, manager_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all feedback submitted by a specific manager, including employee, comments with user details, and tags.
    """
    response = db.table("feedback").select(
        "*, manager:users!feedback_manager_id_fkey(*), employee:users!feedback_employee_id_fkey(*), tags(*)"
    ).eq("manager_id", manager_id).order("created_at", desc=True).execute()
    
    return response.data or []

def get_feedback(db: Client, *, feedback_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves a single piece of feedback by its ID, including all related user, comment, and tag data.
    """
    response = db.table("feedback").select(
        "*, manager:users!feedback_manager_id_fkey(*), employee:users!feedback_employee_id_fkey(*), tags(*)"
    ).eq("id", feedback_id).single().execute()
    
    return response.data

def update_feedback(db: Client, *, db_obj: Dict[str, Any], obj_in: FeedbackUpdate) -> Optional[Dict[str, Any]]:
    """
    Updates a feedback entry in Supabase, including its tags.
    """
    update_data = obj_in.model_dump(exclude_unset=True, exclude={"tag_ids"})
    
    if update_data:
        response = db.table("feedback").update(update_data).eq("id", db_obj['id']).execute()
        if not response.data:
            return None
        # Update the db_obj with the new data
        for key, value in response.data[0].items():
            if key in db_obj:
                db_obj[key] = value

    if obj_in.tag_ids is not None:
        # Delete existing tag associations
        db.table("feedback_tags").delete().eq("feedback_id", db_obj['id']).execute()
        
        # Create new tag associations
        if obj_in.tag_ids:
            feedback_tags_data = [
                {"feedback_id": db_obj['id'], "tag_id": tag_id}
                for tag_id in obj_in.tag_ids
            ]
            db.table("feedback_tags").insert(feedback_tags_data).execute()
            # Fetch the new tags to update the db_obj
            tags_response = db.table("tags").select("*").in_("id", obj_in.tag_ids).execute()
            db_obj["tags"] = tags_response.data if tags_response.data else []
        else:
            db_obj["tags"] = []

    return db_obj

def acknowledge_feedback(db: Client, *, db_obj: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Marks a feedback entry as acknowledged by the employee in Supabase.
    """
    response = db.table("feedback").update({"acknowledged": True}).eq("id", db_obj['id']).execute()

    if not response.data:
        return None
        
    return response.data[0]

def get_feedback_stats_by_manager(db: Client, *, manager_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves aggregated feedback sentiment counts for a manager's team.
    """
    # First, get the manager's team
    team_response = db.table("teams").select("id").eq("manager_id", manager_id).single().execute()
    if not team_response.data:
        return []
    team_id = team_response.data['id']

    # Get all employees in the team
    employees_response = db.table("users").select("id").eq("team_id", team_id).execute()
    if not employees_response.data:
        return []
    employee_ids = [employee['id'] for employee in employees_response.data]

    # Get all feedback for those employees
    feedback_response = db.table("feedback").select("sentiment").in_("employee_id", employee_ids).execute()
    if not feedback_response.data:
        return []

    # Aggregate the stats in Python
    stats = {}
    for feedback in feedback_response.data:
        sentiment = feedback['sentiment']
        stats[sentiment] = stats.get(sentiment, 0) + 1
    
    return [{"sentiment": key, "count": value} for key, value in stats.items()]
