#!/usr/bin/env python3
"""CRUD operations for DevSaver."""

from app.models.engine.db import get_session
from app.models.user import User
from typing import Optional
from app.schemas.user import UserInDB, User as UserSchema

def create_user(username: str, email: str, password_hash: str, fullname: Optional[str] = None) -> UserSchema:
    """Create a new user in the database."""
    with get_session() as session:
        new_user = User(username=username, email=email, password_hash=password_hash, fullname=fullname)
        session.add(new_user)
        session.commit()           # INSERT so id is assigned
        session.refresh(new_user) # reloads from db
        # session.expunge(new_user) No need to expunge here as we are returning the dict
         
        return UserSchema.model_validate(new_user)
    
def get_user_by_username(username: str) -> UserInDB | None:
    """Retrieve a user by their username."""
    with get_session() as session:
        user = session.query(User).filter(User.username == username).first()
        return UserInDB.model_validate(user) if user else None # Using Pydantic model here to prevent detachment issues
    
def get_user_by_email(email: str) -> UserSchema | None:
    """Retrieve a user by their email."""
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        return UserSchema.model_validate(user) if user else None
    
def get_user_by_id(user_id: int) -> UserSchema | None:
    """Retrieve a user by their ID."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return UserSchema.model_validate(user) if user else None
    
def update_user(user_id: int, **kwargs) -> UserSchema | None:
    """Update an existing user."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.add(user)
            session.commit()
            session.refresh(user) # reloads from db
            # session.expunge(user)  # detach safely
            return UserSchema.model_validate(user)
        return None
    
def delete_user(user_id: int) -> bool:
    """Delete a user from the database."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            return True
        return False
    
def list_users() -> list[UserSchema]:
    """List all users in the database."""
    with get_session() as session:
        users = session.query(User).all()
        print(f"DEBUG: Found {len(users)} users")
        for user in users:
            session.refresh(user)
            # session.expunge(user)  # detach safely
        return [UserSchema.model_validate(user) for user in users] if users else []