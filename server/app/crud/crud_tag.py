from typing import List
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagCreate

def get_or_create_tags(db: Session, tags: List[str]) -> List[Tag]:
    """
    For a list of tag names, get existing tags or create new ones.
    """
    db_tags = []
    for tag_name in tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        db_tags.append(tag)
    return db_tags