from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_feedback, crud_user
from app.schemas import feedback as feedback_schema
from app.api import deps
from app.models.user import User as UserModel, Role

router = APIRouter()

@router.post("/", response_model=feedback_schema.Feedback, status_code=status.HTTP_201_CREATED)
def create_feedback(
    *,
    db: Session = Depends(deps.get_db),
    feedback_in: feedback_schema.FeedbackCreate,
    current_user: UserModel = Depends(deps.get_current_manager),
):
    """
    Create new feedback for an employee. (Manager only)
    """
    employee = crud_user.get_user(db, user_id=feedback_in.employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    if not employee.team_id or employee.team.manager_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Can only give feedback to employees in your team."
        )

    feedback = crud_feedback.create_feedback(
        db=db, feedback=feedback_in, manager_id=current_user.id
    )
    return feedback

@router.get("/", response_model=List[feedback_schema.Feedback])
def read_feedback(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Retrieve feedback.
    - Managers see all feedback they have given.
    - Employees see all feedback they have received.
    """
    if current_user.role == Role.manager:
        return crud_feedback.get_feedback_by_manager(db, manager_id=current_user.id)
    else: # Employee
        return crud_feedback.get_feedback_by_employee(db, employee_id=current_user.id)

@router.put("/{feedback_id}", response_model=feedback_schema.Feedback)
def update_feedback(
    feedback_id: int,
    feedback_in: feedback_schema.FeedbackUpdate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_manager),
):
    """
    Update feedback. (Manager who created it only)
    """
    feedback = crud_feedback.get_feedback(db, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.manager_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this feedback")

    return crud_feedback.update_feedback(db=db, db_obj=feedback, obj_in=feedback_in)

@router.patch("/{feedback_id}/acknowledge", response_model=feedback_schema.Feedback)
def acknowledge_feedback(
    feedback_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Acknowledge feedback. (Employee who received it only)
    """
    feedback = crud_feedback.get_feedback(db, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to acknowledge this feedback")

    return crud_feedback.acknowledge_feedback(db=db, db_obj=feedback)
