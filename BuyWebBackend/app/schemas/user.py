from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cho phép chuyển đổi từ SQLAlchemy model
