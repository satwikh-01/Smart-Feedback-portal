from sqlalchemy.orm import relationship

from .user import User
from .team import Team
from .feedback import Feedback, feedback_tags_association
from .comment import Comment
from .tag import Tag
from .notification import Notification

# User relationships
User.managed_team = relationship("Team", back_populates="manager", foreign_keys="[Team.manager_id]")
User.team = relationship("Team", back_populates="members", foreign_keys="[User.team_id]")
User.comments = relationship("Comment", back_populates="user")
User.feedback_given = relationship("Feedback", foreign_keys="[Feedback.manager_id]", back_populates="manager")
User.feedback_received = relationship("Feedback", foreign_keys="[Feedback.employee_id]", back_populates="employee")
User.notifications = relationship("Notification", back_populates="user")

# Team relationships
Team.manager = relationship("User", back_populates="managed_team", foreign_keys="[Team.manager_id]")
Team.members = relationship("User", back_populates="team", foreign_keys="[User.team_id]")

# Feedback relationships
Feedback.employee = relationship("User", foreign_keys=[Feedback.employee_id], back_populates="feedback_received")
Feedback.manager = relationship("User", foreign_keys=[Feedback.manager_id], back_populates="feedback_given")
Feedback.comments = relationship("Comment", back_populates="feedback", cascade="all, delete-orphan")
Feedback.tags = relationship("Tag", secondary=feedback_tags_association, back_populates="feedback_items")

# Comment relationships
Comment.feedback = relationship("Feedback", back_populates="comments")
Comment.user = relationship("User", back_populates="comments")

# Tag relationships
Tag.feedback_items = relationship("Feedback", secondary=feedback_tags_association, back_populates="tags")

# Notification relationships
Notification.user = relationship("User", back_populates="notifications")