from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate, user_id: int) -> Comment:
    """
    Create a new comment on a feedback item.
    """
    db_comment = Comment(
        content=comment.content,
        feedback_id=comment.feedback_id,
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment