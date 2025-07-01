import enum
from pydantic import BaseModel
from typing import List, Optional
import datetime
from .user import User
from .tag import Tag

# Moved the Sentiment Enum from the old models file to here
class Sentiment(str, enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class FeedbackBase(BaseModel):
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    sentiment: Sentiment
    feedback: str

class FeedbackCreate(FeedbackBase):
    employee_id: int
    tag_ids: Optional[List[int]] = []

class FeedbackUpdate(FeedbackBase):
    tag_ids: Optional[List[int]] = None

class FeedbackAcknowledge(BaseModel):
    acknowledged: bool

class Feedback(FeedbackBase):
    id: int
    employee: User
    manager: User
    acknowledged: bool
    created_at: datetime.datetime
    # This field might not exist in your Supabase table, so it's safer to make it optional
    updated_at: Optional[datetime.datetime] = None
    tags: List[Tag] = []

    class Config:
        from_attributes = True
