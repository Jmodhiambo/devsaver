#!/usr/bin/env python3
"""Tests for CRUD operations."""

import pytest
from app.test.conftest import db_session
from app.models.user import User
from app.models.resource import Resource


@pytest.fixture()
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(username="Mart", email="mart@test.com", password_hash="hashedpassword")
    db_session.add(user)
    db_session.commit() # Commit to save the user
    db_session.refresh(user) # Refresh to get updated fields like id
    return user
   

@pytest.fixture()
def sample_resource(db_session, sample_user):
    """Create a sample resource for testing."""
    resource = Resource(
        title="Sample Resource",
        description="A resource for testing",
        tags="test, sample",
        type="article",
        source="example.com",
        read_status=False,
        starred=False,
        url="http://example.com/sample",
        user_id=sample_user.id
    )
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)
    return resource