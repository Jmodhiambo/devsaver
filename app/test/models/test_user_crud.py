#!/usr/bin/env python3
"""Tests for CRUD operations on User model."""

from app.test.conftest import db_session
from app.models.user import User
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

def test_update_user(db_session):
    """Test updating a user."""
    user = UserFactory(username="Jm")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user_to_update = db_session.query(User).filter_by(id=user.id).first()
    user_to_update.username = "Mart"
    db_session.commit()
    db_session.refresh(user_to_update)

    updated_user = db_session.query(User).filter_by(id=user.id).first()
    assert updated_user.username == "Mart"

def test_delete_user(db_session):
    """Test deleting a user."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user_to_delete = db_session.query(User).filter_by(id=user.id).first()
    db_session.delete(user_to_delete)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(id=user.id).first()
    assert deleted_user is None

def test_get_user_by_username(db_session):
    """Test retrieving a user by username."""
    user = UserFactory(username="UniqueUser")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fetched_user = db_session.query(User).filter_by(username="UniqueUser").first()
    assert fetched_user is not None
    assert fetched_user.email == user.email

def test_get_user_by_email(db_session):
    """Test retrieving a user by email."""
    user = UserFactory(email="jm@test.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fetched_user = db_session.query(User).filter_by(email="jm@test.com").first()
    assert fetched_user is not None
    assert fetched_user.username == user.username

def test_list_users(db_session):
    """Test listing all users."""
    user1 = UserFactory()
    user2 = UserFactory()
    db_session.add_all([user1, user2])
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)

    users = db_session.query(User).all()
    assert len(users) >= 2  # At least the two we just added
    usernames = [user.username for user in users]
    assert user1.username in usernames
    assert user2.username in usernames

def test_get_user_by_id(db_session):
    """Test retrieving a user by ID."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fetched_user = db_session.query(User).filter_by(id=user.id).first()
    assert fetched_user is not None
    assert fetched_user.username == user.username
    assert fetched_user.email == user.email