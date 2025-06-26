from pydantic import BaseModel
import datetime

class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True
