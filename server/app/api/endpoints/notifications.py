from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status
from supabase import Client # Replaced Session with Client

from app.crud import crud_notification
from app.schemas import notification as notification_schema
from app.api import deps

# The import for the SQLAlchemy UserModel is no longer needed.
# from app.models.user import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[notification_schema.Notification])
def read_notifications(
    db: Client = Depends(deps.get_db), # Updated type hint
    current_user: Dict[str, Any] = Depends(deps.get_current_user), # Updated type hint
):
    """
    Retrieve all notifications for the current user.
    """
    # Use dictionary key access for user ID
    return crud_notification.get_notifications_by_user(db, user_id=current_user['id'])

@router.patch("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def mark_notification_as_read(
    notification_id: int,
    db: Client = Depends(deps.get_db), # Updated type hint
    current_user: Dict[str, Any] = Depends(deps.get_current_user), # Updated type hint
):
    """
    Mark one of the current user's notifications as read.
    """
    # Use dictionary key access for user ID
    crud_notification.mark_notification_as_read(
        db, notification_id=notification_id, user_id=current_user['id']
    )
    return