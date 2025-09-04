#!/usr/bin/env python3
"""CRUD operations for DevSaver."""

from app.models.engine.db import get_session
from app.models.user import User
from typing import Optional

def create_user(username: str, email: str, password_hash: str, fullname: Optional[str]) -> User:
    """Create a new user in the database."""
    with get_session() as session:
        new_user = User(username=username, email=email, password_hash=password_hash, fullname=fullname)
        session.add(new_user)
        session.commit()           # INSERT so id is assigned
        session.refresh(new_user) # reloads from db
        # session.expunge(new_user) No need to expunge here as we are returning the dict
        print(f"DEBUG: Created user object type = {type(new_user)}")
         
        return new_user.to_dict()
    
def get_user_by_username(username: str) -> User | None:
    """Retrieve a user by their username."""
    with get_session() as session:
        user = session.query(User).filter(User.username == username).first()
        session.refresh(user)
        # session.expunge(user)  # detach safely
        return user.to_dict() if user else None
    
def get_user_by_email(email: str) -> User | None:
    """Retrieve a user by their email."""
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        return user.to_dict() if user else None
    
def get_user_by_id(user_id: int) -> User | None:
    """Retrieve a user by their ID."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        session.refresh(user)
        return user.to_dict() if user else None
    
def update_user(user_id: int, **kwargs) -> User | None:
    """Update an existing user."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.add(user)
            session.flush()
            session.refresh(user) # reloads from db
            # session.expunge(user)  # detach safely
            return user.to_dict()
        return None
    
def delete_user(user_id: int) -> bool:
    """Delete a user from the database."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            return True
        return False
    
def list_users() -> list[User]:
    """List all users in the database."""
    with get_session() as session:
        users = session.query(User).all()
        print(f"DEBUG: Found {len(users)} users")
        for user in users:
            session.refresh(user)
            # session.expunge(user)  # detach safely
        #return users.to_dict() if users else []
        return [user.to_dict() for user in users] if users else []