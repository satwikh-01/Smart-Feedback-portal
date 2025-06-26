from typing import List
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

def create_feedback(db: Session, feedback: FeedbackCreate, manager_id: int) -> Feedback:
    """
    Creates a new feedback entry in the database.
    """
    db_feedback = Feedback(
        **feedback.model_dump(),
        manager_id=manager_id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback_by_employee(db: Session, employee_id: int) -> List[Feedback]:
    """
    Retrieves all feedback for a specific employee.
    """
    return db.query(Feedback).filter(Feedback.employee_id == employee_id).all()

def get_feedback_by_manager(db: Session, manager_id: int) -> List[Feedback]:
    """
    Retrieves all feedback submitted by a specific manager.
    """
    return db.query(Feedback).filter(Feedback.manager_id == manager_id).all()

def get_feedback(db: Session, feedback_id: int) -> Feedback:
    """
    Retrieves a single piece of feedback by its ID.
    """
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

def update_feedback(db: Session, db_obj: Feedback, obj_in: FeedbackUpdate) -> Feedback:
    """
    Updates a feedback entry.
    """
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def acknowledge_feedback(db: Session, db_obj: Feedback) -> Feedback:
    """
    Marks a feedback entry as acknowledged by the employee.
    """
    db_obj.acknowledged = True
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj