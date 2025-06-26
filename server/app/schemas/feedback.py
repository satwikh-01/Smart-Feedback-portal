from pydantic import BaseModel
from typing import List, Optional
import datetime
from .user import User
from .comment import Comment
from .tag import Tag
from app.models.feedback import Sentiment # Import the Enum

class FeedbackBase(BaseModel):
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    sentiment: Sentiment

class FeedbackCreate(FeedbackBase):
    employee_id: int

class FeedbackUpdate(FeedbackBase):
    pass

class FeedbackAcknowledge(BaseModel):
    acknowledged: bool

class Feedback(FeedbackBase):
    id: int
    employee: User
    manager: User
    acknowledged: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    comments: List[Comment] = []
    tags: List[Tag] = []

    class Config:
        from_attributes = True
