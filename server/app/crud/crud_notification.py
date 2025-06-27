from typing import List
from sqlalchemy.orm import Session
from app.models.notification import Notification

def create_notification(db: Session, user_id: int, message: str) -> Notification:
    """
    Create a new notification for a user.
    """
    db_notification = Notification(user_id=user_id, message=message)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications_by_user(db: Session, user_id: int) -> List[Notification]:
    """
    Get all notifications for a specific user.
    """
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()

def mark_notification_as_read(db: Session, notification_id: int, user_id: int) -> Notification:
    """
    Mark a specific notification as read.
    """
    db_notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if db_notification:
        db_notification.is_read = True
        db.commit()
        db.refresh(db_notification)
    return db_notification