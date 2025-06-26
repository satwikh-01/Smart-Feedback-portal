import enum
import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, Text, Table
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.db.base import Base

class Sentiment(str, enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

# Association table for the many-to-many relationship between feedback and tags
feedback_tags_association = Table(
    "feedback_tags",
    Base.metadata,
    Column("feedback_id", Integer, ForeignKey("feedback.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    sentiment = Column(SQLAlchemyEnum(Sentiment))
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    employee = relationship("User", foreign_keys=[employee_id])
    manager = relationship("User", foreign_keys=[manager_id])
    comments = relationship("Comment", back_populates="feedback", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=feedback_tags_association, back_populates="feedback_items")

