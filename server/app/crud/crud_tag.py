from typing import List, Dict, Any
from supabase import Client

# Note: We no longer need imports from sqlalchemy.orm, app.models, or app.schemas for this file.

def get_or_create_tags(db: Client, *, tags: List[str]) -> List[Dict[str, Any]]:
    """
    For a list of tag names, get existing tags or create new ones using Supabase upsert.
    Assumes the 'tags' table has a UNIQUE constraint on the 'name' column.
    """
    if not tags:
        return []

    # Prepare a list of dictionaries for the upsert operation
    tag_data = [{"name": tag_name} for tag_name in tags]
    
    # Use 'upsert' to insert new tags. If a tag with the same name exists, it will be ignored.
    # The 'on_conflict' parameter should match the column with the UNIQUE constraint in your DB.
    response = (
        db.table("tags")
        .upsert(tag_data, on_conflict="name", ignore_duplicates=True)
        .execute()
    )

    # After upserting, we need to fetch all the tags to return their full objects, including IDs.
    # The 'in_' filter is perfect for fetching multiple records based on a list of values.
    fetch_response = db.table("tags").select("*").in_("name", tags).execute()
    
    return fetch_response.data if fetch_response.data else []