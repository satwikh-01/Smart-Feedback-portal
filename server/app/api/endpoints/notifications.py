from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import crud_notification
from app.schemas import notification as notification_schema
from app.api import deps
from app.models.user import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[notification_schema.Notification])
def read_notifications(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Retrieve all notifications for the current user.
    """
    return crud_notification.get_notifications_by_user(db, user_id=current_user.id)

@router.patch("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Mark one of the current user's notifications as read.
    """
    crud_notification.mark_notification_as_read(
        db, notification_id=notification_id, user_id=current_user.id
    )
    return