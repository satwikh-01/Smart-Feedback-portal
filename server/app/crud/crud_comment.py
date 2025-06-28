from typing import Dict, Any, Optional
from supabase import Client
from app.schemas.comment import CommentCreate

# Note: We no longer need imports from sqlalchemy.orm or app.models

def create_comment(db: Client, *, comment: CommentCreate, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Create a new comment on a feedback item using Supabase.
    """
    # Create a dictionary from the input schema and user_id
    comment_data = {
        "content": comment.content,
        "feedback_id": comment.feedback_id,
        "user_id": user_id
    }
    
    # Insert the new comment data into the 'comments' table
    response = db.table("comments").insert(comment_data).execute()

    if not response.data:
        # The insert operation failed or returned no data
        return None
        
    # Supabase returns the inserted data in a list
    return response.data[0]