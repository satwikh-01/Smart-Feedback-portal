from fastapi import APIRouter, Depends, Body
from typing import List, Dict, Any
from app.services import gemini_service
from app.api import deps
from supabase import Client
from app.crud import crud_tag

# The import for the SQLAlchemy UserModel is no longer needed.
# from app.models.user import User as UserModel

router = APIRouter()

@router.post("/suggest-feedback", response_model=str)
def suggest_feedback(
    prompt: str = Body(..., embed=True), 
    current_user: Dict[str, Any] = Depends(deps.get_current_user)
):
    return gemini_service.generate_feedback_suggestion(prompt)

@router.post("/rephrase", response_model=str)
def rephrase(
    text: str = Body(..., embed=True), 
    current_user: Dict[str, Any] = Depends(deps.get_current_user)
):
    return gemini_service.rephrase_text(text)

@router.post("/suggest-tags", response_model=Dict[str, List[int]])
def suggest_tags(
    db: Client = Depends(deps.get_db),
    text: str = Body(..., embed=True),
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Suggests tags for a piece of feedback and returns their IDs.
    """
    suggested_tag_names = gemini_service.suggest_tags_for_feedback(text)
    
    if not suggested_tag_names:
        return {"tag_ids": []}

    # This will create any new tags and fetch existing ones.
    tags = crud_tag.get_or_create_tags(db, tags=suggested_tag_names)
    
    # Return a list of tag IDs
    tag_ids = [tag['id'] for tag in tags]
    return {"tag_ids": tag_ids}

@router.post("/generate-feedback", response_model=Dict[str, Any])
def generate_feedback(
    db: Client = Depends(deps.get_db),
    strengths: str = Body(...),
    areas_for_improvement: str = Body(...),
    current_user: Dict[str, Any] = Depends(deps.get_current_manager),
):
    """
    Generates a complete feedback entry, including sentiment and tags.
    """
    # Generate the feedback text
    feedback_text = gemini_service.generate_comprehensive_feedback(strengths, areas_for_improvement)
    
    # Determine the sentiment
    sentiment = gemini_service.analyze_sentiment(feedback_text)
    
    # Suggest tags
    suggested_tag_names = gemini_service.suggest_tags_for_feedback(feedback_text)
    tags = crud_tag.get_or_create_tags(db, tags=suggested_tag_names)
    tag_ids = [tag['id'] for tag in tags]
    
    return {
        "feedback": feedback_text,
        "sentiment": sentiment,
        "tag_ids": tag_ids,
    }
