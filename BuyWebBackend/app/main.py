from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
from .core.database import engine, SessionLocal
from sqlalchemy.exc import IntegrityError
from .models import Base
from .models.user import User
from .schemas.user import UserCreate, UserResponse
from .api.v1.router import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/", response_model=List[UserResponse])
def read_root():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()



