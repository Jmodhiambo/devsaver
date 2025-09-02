#!/usr/bin/env python3
"""Tests for CRUD operations on User model."""

from app.test.conftest import db_session
from app.models.user import User
# from app.test.models.conftest import sample_user
from app.test.factories.user_factory import UserFactory


def test_create_user(db_session):
    """Test creating a new user."""
    new_user = User(username="Mart", email="mart@test.com", password_hash="hashedpassword")
    db_session.add(new_user)
    db_session.commit() # Commit to save the user
    db_session.refresh(new_user) # Refresh to get updated fields like id

    user = db_session.query(User).filter_by(username="Mart").first()
    assert user is not None
    assert user.email == "mart@test.com"
    assert user.password_hash == "hashedpassword"    

def test_read_user(db_session):
    """Test reading a user."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user) # Refresh to get updated fields like id

    fetched_user = db_session.query(User).filter_by(id=user.id).first()
    assert fetched_user is not None
    assert fetched_user.username == user.username
    assert fetched_user.email == user.email
    assert user.id is not None
