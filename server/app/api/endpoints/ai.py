from fastapi import APIRouter, Depends, Body
from typing import List
from app.services import gemini_service
from app.api import deps
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/suggest-feedback", response_model=str)
def suggest_feedback(prompt: str = Body(..., embed=True), current_user: UserModel = Depends(deps.get_current_user)):
    return gemini_service.generate_feedback_suggestion(prompt)

@router.post("/rephrase", response_model=str)
def rephrase(text: str = Body(..., embed=True), current_user: UserModel = Depends(deps.get_current_user)):
    return gemini_service.rephrase_text(text)

@router.post("/suggest-tags", response_model=List[str])
def suggest_tags(
    strengths: str = Body(...),
    areas_for_improvement: str = Body(...),
    current_user: UserModel = Depends(deps.get_current_manager),
):
    return gemini_service.suggest_tags_for_feedback(strengths, areas_for_improvement)
