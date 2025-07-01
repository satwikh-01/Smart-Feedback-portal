from typing import Generator, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from supabase import Client # Import Supabase Client

from app.core import security
from app.core.config import settings
from app.db.session import supabase # Import Supabase client instead of SessionLocal
from app.crud import crud_user

# SQLAlchemy models and Session are no longer needed
# from sqlalchemy.orm import Session
# from app.models.user import User, Role

# This defines the URL where the client will send the username and password to get a token
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

def get_db() -> Generator[Client, None, None]:
    """
    A dependency that provides a Supabase client instance for each request.
    """
    try:
        yield supabase
    finally:
        # With the Supabase client, we don't need to manually close a session.
        pass

def get_current_user(
    db: Client = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Dict[str, Any]:
    """
    Dependency to get the current user from a JWT token.
    The user is returned as a dictionary.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials, user ID not in token",
            )
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Use the modified CRUD function to get the user from Supabase
    user = crud_user.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_manager(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to check if the current user is a manager.
    The user is a dictionary.
    """
    # Use dictionary key access to check the role
    if current_user.get('role') != 'manager':
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_employee(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to check if the current user is an employee.
    The user is a dictionary.
    """
    if current_user.get('role') != 'employee':
        raise HTTPException(
            status_code=403, detail="This action is only available to employees."
        )
    return current_user
