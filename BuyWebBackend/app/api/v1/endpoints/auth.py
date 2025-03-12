from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, UserAuth
from app.services.auth import AuthService   
from app.services.auth import oauth2_scheme
from fastapi import Depends



router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return AuthService.register_new_user(db, user_data) 

@router.post("/login", response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user.
    """
    return AuthService.login_user(db, user_data)

@router.post("/refresh", response_model=Token)
def refresh_token( refresh_token: str = Depends(oauth2_scheme)):
    """
    Refresh an access token.
    """
    return AuthService.refresh_token(refresh_token)


@router.get("/me", response_model=UserAuth)
def get_current_user(current_user: UserAuth = Depends(AuthService.get_current_user)):
    """
    Get details of currently authenticated user.
    """
    return current_user  









