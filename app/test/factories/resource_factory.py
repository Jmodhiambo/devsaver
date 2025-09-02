#!/usr/bin/env python3
"""Factories for creating test resources."""

import factory
from app.models.resource import Resource

class ResourceFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Resource instances."""

    class Meta:
        model = Resource
        sqlalchemy_session_persistence = 'flush'  # Use 'flush' to avoid committing in tests
        sqlalchemy_session = None  # This will be set in the test setup

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph', nb_sentences=3)
    tags = factory.Faker('words', nb=3, ext_word_list=['python', 'orm', 'sqlalchemy', 'flask', 'testing'])
    type = factory.Faker('random_element', elements=['article', 'video', 'book', 'tutorial', 'image', 'podcast'])
    source = factory.Faker('url')
    url = factory.Faker('url')
    read_status = factory.Faker('boolean')
    starred = factory.Faker('boolean')
    created_at = factory.Faker('date_time_this_year', tzinfo=None)
    updated_at = factory.Faker('date_time_this_year', tzinfo=None)
    user_id = factory.SubFactory('app.test.factories.user_factory.UserFactory', id=factory.SelfAttribute('..user_id'))

# Note: The user_id field uses a SubFactory to link to a UserFactory instance.