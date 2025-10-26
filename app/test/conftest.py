#!/usr/bin/env python3
"""Tests for CRUD operations."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.resource import Resource


@pytest.fixture()
def db_session():
    """Create a new database session for a test."""
    # Use an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback() # ensure any changes are rolled back
        session.close()
        engine.dispose() # Dispose the engine to free resources

@pytest.fixture(autouse=True)
def set_factory_session(db_session, monkeypatch):
    """Automatically set the session for all factories to use the test db_session."""
    from app.test.factories.user_factory import UserFactory
    from app.test.factories.resource_factory import ResourceFactory

    # Patch the _meta.session attribute of each factory to use the db_session
    monkeypatch.setattr(UserFactory._meta, 'sqlalchemy_session', db_session)
    monkeypatch.setattr(ResourceFactory._meta, 'sqlalchemy_session', db_session)