from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from supabase import Client

from app.crud import crud_user
from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.core import security
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=user_schema.User)
def register_user(
    *,
    db: Client = Depends(deps.get_db),
    user_in: user_schema.UserCreate,
):
    """
    Create a new user.
    - If role is 'manager', a 'team_name' must be provided to create a new team.
    - If role is 'employee', a 'team_id' must be provided to assign to a team.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system.",
        )
    
    try:
        # Call the new, updated CRUD function
        user = crud_user.create_user_with_team(db=db, user_in=user_in)
        if not user:
            # This case handles unexpected failures from the CRUD function
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred during user creation.",
            )
    except ValueError as e:
        # Handle specific validation errors from the CRUD function
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle other potential exceptions during the creation process
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
        
    return user


@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(
    db: Client = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    if not user or not security.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = security.create_access_token(subject=user['id'])
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
