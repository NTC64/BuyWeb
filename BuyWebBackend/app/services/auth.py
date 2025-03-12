from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends      
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import PyJWTError
import secrets
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token, UserAuth
from app.core.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = secrets.token_hex(64)
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(user_id: int) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    

    @staticmethod       
    def create_refresh_token(user_id: int) -> str:
        
        payload = {
            "sub": user_id,
            "exp": datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    




    @staticmethod
    def register_new_user(db: Session, user_data: UserCreate) -> User:
        # Verify if passwords match
        if user_data.password != user_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        # Check if user already exists
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create new user
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=AuthService.get_password_hash(user_data.password)
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user 
    
    @staticmethod
    def login_user(db: Session, user_data: UserLogin) -> Token:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not AuthService.verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        access_token = AuthService.create_access_token(user.id)
        refresh_token = AuthService.create_refresh_token(user.id)
        return Token(access_token=access_token, refresh_token=refresh_token)
    
    @staticmethod
    def refresh_token(refresh_token: str) -> Token:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            
            access_token = AuthService.create_access_token(user.id)
            refresh_token = AuthService.create_refresh_token(user.id)
            return Token(access_token=access_token, refresh_token=refresh_token)
        except jwt.JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    @staticmethod
    def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserAuth: 
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            return UserAuth.model_validate(user)
        except PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
