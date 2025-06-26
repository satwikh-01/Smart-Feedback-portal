import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    feedback = relationship("Feedback", back_populates="comments")
    user = relationship("User")
