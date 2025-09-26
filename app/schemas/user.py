#!/usr/bin/env python3
"""Schema definitions for user-related data."""
from pydantic import BaseModel, EmailStr, field_serializer, constr
from typing import Optional, Annotated
from datetime import datetime as datatime
from app.utils.pydantic.schema import as_form

@as_form
class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    username: Annotated[str, constr(min_length=3)]
    fullname: Optional[str] = None

    class Config:
        from_attributes = True


@as_form
class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: Annotated[str, constr(min_length=8)]

    class Config:
        from_attributes = True

@as_form
class UserUpdate(BaseModel):
    """Schema for updating user information."""
    fullname: Optional[str] = None
    password: Optional[Annotated[str, constr(min_length=8)]] = None

    class Config:
        from_attributes = True
        
@as_form
class UserInDBBase(UserBase):
    """Base schema for user data stored in the database."""
    id: int
    created_at: datatime
    updated_at: datatime
    last_login_at: Optional[datatime] = None
    deleted_at: Optional[datatime] = None

    @field_serializer("created_at", "updated_at", "last_login_at", "deleted_at")
    def serialize_datetime(self, value: datatime | None) -> Optional[str]:
        """Serialize datetime fields to ISO format strings."""
        return value.isoformat() if value else None

    class Config:
        from_attributes = True

@as_form
class UserInDB(UserInDBBase):
    """Schema for user data stored in the database, including password hash."""
    password_hash: str

    class Config:
        from_attributes = True

@as_form
class User(UserInDBBase):
    """Schema for user data returned to clients."""
    pass

@as_form
class UserPublic(BaseModel):
    """Schema for public user data."""
    id: int
    username: str
    fullname: Optional[str] = None

    class Config:
        from_attributes = True

@as_form
class UserLogin(BaseModel):
    """Schema for user login."""
    username: Annotated[str, constr(min_length=3)]
    password: Annotated[str, constr(min_length=8)]

    class Config:
        from_attributes = True


@as_form
class PasswordChange(BaseModel):
    """Schema for changing user password."""
    old_password: Annotated[str, constr(min_length=8)]
    new_password: Annotated[str, constr(min_length=8)]

    class Config:
        from_attributes = True

@as_form
class PasswordResetRequest(BaseModel):
    """Schema for requesting a password reset."""
    email: EmailStr
    redirect_url: Optional[str] = None

    class Config:
        from_attributes = True