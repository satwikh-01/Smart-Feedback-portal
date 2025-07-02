from fastapi.responses import StreamingResponse
from app.services import pdf_service
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client # Replaced Session with Client
from app.crud import crud_feedback, crud_user, crud_notification, crud_team
from app.schemas import feedback as feedback_schema
from app.api import deps

# Note: UserModel and Role are no longer imported from app.models

router = APIRouter()

@router.post("/", response_model=feedback_schema.Feedback, status_code=status.HTTP_201_CREATED)
def create_feedback(
    *,
    db: Client = Depends(deps.get_db),
    feedback_in: feedback_schema.FeedbackCreate,
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Create new feedback for an employee. (Manager only)
    """
    employee = crud_user.get_user(db, user_id=feedback_in.employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    # With Supabase, we must manually check the team relationship
    if not employee.get("team_id"):
        raise HTTPException(
            status_code=403, detail="Employee is not assigned to any team."
        )
    
    # We will need to create/modify crud_team.get_team in a later step
    team = crud_team.get_team(db, team_id=employee["team_id"])
    if not team or team["manager_id"] != current_user["id"]:
         raise HTTPException(
            status_code=403, detail="Can only give feedback to employees in your team."
        )

    new_feedback = crud_feedback.create_feedback(
        db=db, feedback_in=feedback_in, manager_id=current_user["id"]
    )

    # Create a notification for the employee
    crud_notification.create_notification(
        db,
        user_id=new_feedback['employee_id'],
        message=f"You have new feedback from {current_user['full_name']}."
    )

    # Re-fetch the feedback to include all relationships
    return crud_feedback.get_feedback(db, feedback_id=new_feedback['id'])

@router.get("/", response_model=List[feedback_schema.Feedback])
def read_feedback(
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_user),
):
    """
    Retrieve feedback.
    - Managers see all feedback they have given.
    - Employees see all feedback they have received.
    """
    # Use dictionary access for 'role' and 'id'
    if current_user['role'] == 'manager':
        return crud_feedback.get_feedback_by_manager(db, manager_id=current_user['id'])
    else: # Employee
        return crud_feedback.get_feedback_by_employee(db, employee_id=current_user['id'])

@router.put("/{feedback_id}", response_model=feedback_schema.Feedback)
def update_feedback(
    feedback_id: int,
    feedback_in: feedback_schema.FeedbackUpdate,
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Update feedback. (Manager who created it only)
    """
    feedback = crud_feedback.get_feedback(db, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback['manager_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized to update this feedback")

    return crud_feedback.update_feedback(db=db, db_obj=feedback, obj_in=feedback_in)

@router.patch("/{feedback_id}/acknowledge", response_model=feedback_schema.Feedback)
def acknowledge_feedback(
    feedback_id: int,
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_user),
):
    """
    Acknowledge feedback. (Employee who received it only)
    """
    feedback = crud_feedback.get_feedback(db, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback['employee_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized to acknowledge this feedback")

    crud_feedback.acknowledge_feedback(db=db, db_obj=feedback)

    # Notify the manager
    crud_notification.create_notification(
        db,
        user_id=feedback['manager_id'],
        message=f"{current_user['full_name']} has acknowledged your feedback."
    )

    # Re-fetch the feedback to ensure the response model is satisfied
    return crud_feedback.get_feedback(db, feedback_id=feedback_id)

@router.post("/request", status_code=status.HTTP_202_ACCEPTED)
def request_feedback(
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_employee),
):
    """
    Allows an employee to request feedback from their manager.
    """
    if not current_user.get("team_id"):
        raise HTTPException(status_code=400, detail="You are not in a team.")

    team = crud_team.get_team(db, team_id=current_user["team_id"])
    if not team or not team.get("manager_id"):
        raise HTTPException(status_code=404, detail="Your manager could not be found.")

    crud_notification.create_notification(
        db,
        user_id=team["manager_id"],
        message=f"Your team member, {current_user['full_name']}, has requested feedback."
    )
    return {"message": "Feedback request sent successfully"}


@router.get("/export/pdf", response_class=StreamingResponse)
def export_feedback_as_pdf(
    db: Client = Depends(deps.get_db),
    current_user: Dict[str, Any] = Depends(deps.get_current_user),
):
    """
    Export all of a user's feedback (given or received) as a PDF.
    """
    if current_user['role'] == 'manager':
        feedback_list = crud_feedback.get_feedback_by_manager(db, manager_id=current_user['id'])
    else: # Employee
        feedback_list = crud_feedback.get_feedback_by_employee(db, employee_id=current_user['id'])

    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback found to export.")

    # Assumes pdf_service.create_feedback_pdf can handle a list of dictionaries
    pdf_buffer = pdf_service.create_feedback_pdf(feedback_list)

    headers = {'Content-Disposition': 'attachment; filename="feedback_report.pdf"'}
    return StreamingResponse(pdf_buffer, media_type='application/pdf', headers=headers)
