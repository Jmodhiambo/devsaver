#!/usr/bin/env python3
"""Factories for creating test users."""

import factory
from app.models.user import User

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User
        sqlalchemy_session = None  # This will be set in the test setup
        sqlalchemy_session_persistence = 'flush' # Use 'flush' to avoid committing in tests

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password_hash = factory.Faker('password')