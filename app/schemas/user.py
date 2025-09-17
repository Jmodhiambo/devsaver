#!/usr/bin/env python3
"""Schema definitions for user-related data."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime as datatime

class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    username: str
    fullname: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating user information."""
    fullname: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True
        
class UserInDBBase(UserBase):
    """Base schema for user data stored in the database."""
    id: int
    created_at: datatime
    updated_at: datatime
    last_login_at: Optional[datatime] = None
    deleted_at: Optional[datatime] = None

    class Config:
        from_attributes = True

class UserInDB(UserInDBBase):
    """Schema for user data stored in the database, including password hash."""
    password_hash: str

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Schema for user data returned to clients."""
    pass

class UserPublic(BaseModel):
    """Schema for public user data."""
    id: int
    username: str
    fullname: Optional[str] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for changing user password."""
    old_password: str
    new_password: str

    class Config:
        from_attributes = True

class PasswordResetRequest(BaseModel):
    """Schema for requesting a password reset."""
    email: EmailStr
    redirect_url: Optional[str] = None

    class Config:
        from_attributes = True