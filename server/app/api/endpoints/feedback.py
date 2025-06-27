from fastapi.responses import StreamingResponse
from app.services import pdf_service
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import crud_feedback, crud_user, crud_comment, crud_notification
from app.schemas import feedback as feedback_schema
from app.api import deps
from app.models.user import User as UserModel, Role
from app.schemas import comment as comment_schema

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

@router.post("/{feedback_id}/comments", response_model=comment_schema.Comment)
def create_comment_on_feedback(
    feedback_id: int,
    comment_in: comment_schema.CommentCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Create a comment on a specific feedback item.
    Accessible by the manager who gave the feedback or the employee who received it.
    """
    feedback = crud_feedback.get_feedback(db, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if not (feedback.manager_id == current_user.id or feedback.employee_id == current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to comment on this feedback")

    # Ensure the feedback_id in the payload matches the path
    comment_in.feedback_id = feedback_id
    comment = crud_comment.create_comment(db, comment=comment_in, user_id=current_user.id)

    # Notify the other party
    if current_user.id == feedback.employee_id:
        # Employee commented, notify manager
        notification_recipient_id = feedback.manager_id
    else:
        # Manager commented, notify employee
        notification_recipient_id = feedback.employee_id

    crud_notification.create_notification(
        db,
        user_id=notification_recipient_id,
        message=f"{current_user.full_name} commented on your feedback."
    )

    return comment

@router.get("/export/pdf", response_class=StreamingResponse)
def export_feedback_as_pdf(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Export all of a user's feedback (given or received) as a PDF.
    """
    if current_user.role == Role.manager:
        feedback_list = crud_feedback.get_feedback_by_manager(db, manager_id=current_user.id)
    else: # Employee
        feedback_list = crud_feedback.get_feedback_by_employee(db, employee_id=current_user.id)

    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback found to export.")

    pdf_buffer = pdf_service.create_feedback_pdf(feedback_list)

    headers = {'Content-Disposition': 'attachment; filename="feedback_report.pdf"'}
    return StreamingResponse(pdf_buffer, media_type='application/pdf', headers=headers)


