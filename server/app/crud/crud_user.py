from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> User:
    """
    Fetches a user from the database by their email address.
    :param db: The database session.
    :param email: The user's email.
    :return: The User object or None if not found.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    :param db: The database session.
    :param user: The user data from the UserCreate schema.
    :return: The newly created User object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> User:
    """
    Fetches a user from the database by their ID.
    """
    return db.query(User).filter(User.id == user_id).first()
