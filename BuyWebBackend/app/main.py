from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
from .core.database import User, Session
from .schemas.user import UserCreate, UserResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL của frontend
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các HTTP methods
    allow_headers=["*"],  # Cho phép tất cả các headers
)

@app.get("/", response_model=List[UserResponse])
def read_root():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

@app.post("/users", response_model=dict)
def create_user(user: UserCreate):
    session = Session()
    try:
        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            address=user.address,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            role="user"
        )
        session.add(new_user)
        session.commit()
        return {"message": "User created successfully"}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        session.close()
