from pydantic import BaseModel, EmailStr, constr, Field     
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=8)
    confirm_password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: int
    exp: datetime
    email: EmailStr
    username: str

class TokenData(BaseModel):
    email: EmailStr
    username: str   

class UserAuth(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True          
