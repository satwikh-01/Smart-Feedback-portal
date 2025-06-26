from pydantic import BaseModel
import datetime
from .user import User

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    feedback_id: int

class Comment(CommentBase):
    id: int
    created_at: datetime.datetime
    user: User # The user who wrote the comment

    class Config:
        from_attributes = True