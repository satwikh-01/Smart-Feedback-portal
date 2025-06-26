from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.feedback import feedback_tags_association

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    feedback_items = relationship(
        "Feedback", secondary=feedback_tags_association, back_populates="tags"
    )
