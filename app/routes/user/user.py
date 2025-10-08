#!/usr/bin/env python3
"""Users API routes."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.schemas.user import User as UserSchema
from app.services.user_services import list_all_users, get_user_profile
from app.utils.auth.session import check_current_user


router = APIRouter()

@router.get("/users/", response_model=list[UserSchema])
def list_users(sesssion_user: str = Depends(check_current_user)):
    """Retrieve all users."""
    if not sesssion_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    users = list_all_users()
    if not users:
        return JSONResponse(content={"message": "No users found"}, status_code=404)
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, session_user: str = Depends(check_current_user)):
    """Retrieve a user by ID."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    user = get_user_profile(user_id)
    if not user:
        return JSONResponse(content={"message": f"User with id {user_id} not found"}, status_code=404)
    return user