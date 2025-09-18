#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service layer for user-related operations."""

from passlib.hash import argon2
from typing import List, Optional
from app.models.user_crud import (
    create_user, get_user_by_username, get_user_by_email,
    get_user_by_id, update_user, delete_user, list_users
)

def register_user(username: str, email: str, password: str, fullname: Optional[str] = None) -> dict:
    """Register a new user with unique username and email."""
    if get_user_by_username(username):
        raise ValueError(f"The username '{username}' is already taken")
    
    if '@' not in email or '.' not in email:
        raise ValueError("Invalid email format")
    
    if get_user_by_email(email):
        raise ValueError("Email already exists")
    password_hash = argon2.hash(password)
    return create_user(username, email, password_hash, fullname)

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate a user by username and password."""
    user = get_user_by_username(username)
    if user and argon2.verify(password, user.password_hash):
        return user.model_dump(exclude={"password_hash"}) # Exclude password hash from returned data
    return None

def get_user_profile(user_id: int) -> Optional[dict]:
    """Get user profile by user ID."""
    return get_user_by_id(user_id)

def update_user_profile(user_id: int, **kwargs) -> Optional[dict]:
    """Update user profile."""
    if 'email' in kwargs:
        if '@' not in kwargs['email'] or '.' not in kwargs['email']:
            raise ValueError("Invalid email format!")
        existing_user = get_user_by_email(kwargs['email'])
        if existing_user and existing_user['id'] != user_id:
            raise ValueError("Email already exists!")
        
    if 'username' in kwargs:
        existing_user = get_user_by_username(kwargs['username'])
        if existing_user and existing_user['id'] != user_id:
            raise ValueError(f"Username {kwargs['username']} already taken!")

    if 'password' in kwargs:
        kwargs['password_hash'] = argon2.hash(kwargs.pop('password'))
    return update_user(user_id, **kwargs)

def remove_user(user_id: int) -> bool:
    """Remove a user by user ID."""
    return delete_user(user_id)

def list_all_users() -> List[dict]:
    """List all users."""
    return [user.model_dump() for user in list_users()] 

def get_user_by_email_service(email: str) -> Optional[dict]:
    """Get user by email."""
    return get_user_by_email(email)

def get_user_by_username_service(username: str) -> Optional[dict]:
    """Get user by username."""
    return get_user_by_username(username)