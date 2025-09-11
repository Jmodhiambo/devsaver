#!/usr/bin/env python3
"""Users API routes."""

from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.user import User as UserSchema
from app.services.user_services import list_all_users, get_user_profile


router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def list_users():
    """Retrieve all users."""
    users = list_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int):
    """Retrieve a user by ID."""
    user = get_user_profile(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user