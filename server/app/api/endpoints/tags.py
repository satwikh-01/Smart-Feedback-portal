from typing import List
from fastapi import APIRouter, Depends
from supabase import Client
from app.crud import crud_tag
from app.schemas import tag as tag_schema
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[tag_schema.Tag])
def read_tags(
    db: Client = Depends(deps.get_db),
):
    """
    Retrieve all tags.
    """
    return crud_tag.get_all_tags(db)
