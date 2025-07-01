from typing import List, Dict, Any, Optional
from supabase import Client
# Note: We no longer need imports from sqlalchemy.orm or app.models

def create_notification(db: Client, *, user_id: int, message: str) -> Optional[Dict[str, Any]]:
    """
    Create a new notification for a user in Supabase.
    """
    notification_data = {"user_id": user_id, "message": message}
    
    response = db.table("notifications").insert(notification_data).execute()
    
    if not response.data:
        return None
        
    return response.data[0]

def get_notifications_by_user(db: Client, *, user_id: int) -> List[Dict[str, Any]]:
    """
    Get all notifications for a specific user from Supabase.
    """
    response = db.table("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return response.data if response.data else []

def mark_notification_as_read(db: Client, *, notification_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Mark a specific notification as read in Supabase.
    This action is atomic and only targets the specific notification for the user.
    """
    response = (
        db.table("notifications")
        .update({"is_read": True})
        .eq("id", notification_id)
        .eq("user_id", user_id) # Ensures a user can only mark their own notifications
        .execute()
    )
        
    if not response.data:
        return None

    return response.data[0]
