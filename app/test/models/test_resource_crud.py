#!/usr/bin/env python3
"""Tests for CRUD operations on Resource model."""

from app.test.conftest import db_session
from app.models.resource import Resource
from app.test.factories.resource_factory import ResourceFactory
from app.test.factories.user_factory import UserFactory

def test_create_resource(db_session):
    """Test creating a new resource."""
    new_resource = Resource(
        title="Sample Resource",
        description="A resource for testing",
        tags="test, sample",
        type="article",
        source="example.com",
        read_status=False,
        starred=False,
        url="http://example.com/sample",
        user_id=1  # Assuming a user with ID 1 exists for testing purposes
    )
    db_session.add(new_resource)
    db_session.commit() # Commit to save the resource
    db_session.refresh(new_resource) # Refresh to get updated fields like id

    resource = db_session.query(Resource).filter_by(title="Sample Resource").first()
    assert resource is not None
    assert resource.url == "http://example.com/sample"
    assert resource.description == "A resource for testing"

def test_read_resource(db_session):
    """Test reading a resource."""
    resource = ResourceFactory(title="Read Test Resource")
    db_session.add(resource)
    db_session.commit()

    fetched_resource = db_session.query(Resource).filter_by(title="Read Test Resource").first()
    assert fetched_resource is not None
    assert fetched_resource.title == "Read Test Resource"

def test_update_resource(db_session):
    """Test updating a resource."""
    resource = ResourceFactory(title="Update Test Resource", description="Old Description")
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Update Test Resource").first()
    resource_to_update.description = "Updated Description"
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="Update Test Resource").first()
    assert updated_resource.description == "Updated Description"

def test_delete_resource(db_session):
    """Test deleting a resource."""
    resource = ResourceFactory(title="Delete Test Resource")
    db_session.add(resource)
    db_session.commit()

    resource_to_delete = db_session.query(Resource).filter_by(title="Delete Test Resource").first()
    db_session.delete(resource_to_delete)
    db_session.commit()

    deleted_resource = db_session.query(Resource).filter_by(title="Delete Test Resource").first()
    assert deleted_resource is None

def test_list_resources(db_session):
    """Test listing all resources."""
    resource1 = ResourceFactory(title="List Test Resource 1")
    resource2 = ResourceFactory(title="List Test Resource 2")
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.commit()

    resources = db_session.query(Resource).all()
    assert len(resources) >= 2
    titles = [res.title for res in resources]
    assert "List Test Resource 1" in titles
    assert "List Test Resource 2" in titles

def test_filter_resources_by_tag(db_session):
    """Test filtering resources by tag."""
    resource1 = ResourceFactory(title="Tag Test Resource 1", tags="tag1, tag2")
    resource2 = ResourceFactory(title="Tag Test Resource 2", tags="tag2, tag3")
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.commit()

    tagged_resources = db_session.query(Resource).filter(Resource.tags.contains("tag2")).all()
    assert len(tagged_resources) == 2
    titles = [res.title for res in tagged_resources]
    assert "Tag Test Resource 1" in titles
    assert "Tag Test Resource 2" in titles

def test_mark_resource_as_read(db_session):
    """Test marking a resource as read."""
    resource = ResourceFactory(title="Read Status Test Resource", read_status=False)
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Read Status Test Resource").first()
    resource_to_update.read_status = True
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="Read Status Test Resource").first()
    assert updated_resource.read_status is True

def test_star_resource(db_session):
    """Test starring a resource."""
    resource = ResourceFactory(title="Star Test Resource", starred=False)
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Star Test Resource").first()
    resource_to_update.starred = True
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="Star Test Resource").first()
    assert updated_resource.starred is True

def test_unstar_resource(db_session):
    """Test unstarring a resource."""
    resource = ResourceFactory(title="Unstar Test Resource", starred=True)
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Unstar Test Resource").first()
    resource_to_update.starred = False
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="Unstar Test Resource").first()
    assert updated_resource.starred is False

def test_bulk_create_resources(db_session):
    """Test bulk creating resources."""
    resources = [
        ResourceFactory(title="Bulk Resource 1"),
        ResourceFactory(title="Bulk Resource 2"),
        ResourceFactory(title="Bulk Resource 3")
    ]
    db_session.add_all(resources)
    db_session.commit()

    all_resources = db_session.query(Resource).filter(Resource.title.in_(
        ["Bulk Resource 1", "Bulk Resource 2", "Bulk Resource 3"]
    )).all()
    assert len(all_resources) == 3  # Ensure all resources were created


def test_bulk_delete_resources(db_session):
    """Test bulk deleting resources."""
    resource1 = ResourceFactory(title="Bulk Delete Resource 1")
    resource2 = ResourceFactory(title="Bulk Delete Resource 2")
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.commit()

    resources_to_delete = db_session.query(Resource).filter(Resource.title.in_(
        ["Bulk Delete Resource 1", "Bulk Delete Resource 2"]
    )).all()
    for res in resources_to_delete:
        db_session.delete(res)
    db_session.commit()

    deleted_resources = db_session.query(Resource).filter(Resource.title.in_(
        ["Bulk Delete Resource 1", "Bulk Delete Resource 2"]
    )).all()
    assert len(deleted_resources) == 0  # Ensure resources were deleted

def test_update_resource_tags(db_session):
    """Test updating resource tags."""
    resource = ResourceFactory(title="Tag Update Test Resource", tags="oldtag")
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Tag Update Test Resource").first()
    resource_to_update.tags = "newtag1, newtag2"
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="Tag Update Test Resource").first()
    assert updated_resource.tags == "newtag1, newtag2"

def test_filter_resources_by_type(db_session):
    """Test filtering resources by type."""
    resource1 = ResourceFactory(title="Type Test Resource 1", type="article")
    resource2 = ResourceFactory(title="Type Test Resource 2", type="video")
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.commit()

    article_resources = db_session.query(Resource).filter_by(type="article").all()
    assert len(article_resources) == 1
    assert article_resources[0].title == "Type Test Resource 1"

def test_get_resource_by_url(db_session):
    """Test retrieving a resource by URL."""
    resource = ResourceFactory(title="URL Test Resource", url="http://example.com/urltest")
    db_session.add(resource)
    db_session.commit()

    fetched_resource = db_session.query(Resource).filter_by(url="http://example.com/urltest").first()
    assert fetched_resource is not None
    assert fetched_resource.title == "URL Test Resource"

def test_get_resources_by_user_id(db_session):
    """Test retrieving resources by user ID."""
    user = UserFactory() # Create a user to associate with resources
    db_session.add(user)
    db_session.commit()

    resource1 = ResourceFactory(title="User Resource 1", user=user)
    resource2 = ResourceFactory(title="User Resource 2", user=user)
    db_session.add_all([resource1, resource2])
    db_session.commit()

    user_resources = db_session.query(Resource).filter_by(user_id=user.id).all()
    assert len(user_resources) == 2
    titles = [res.title for res in user_resources]
    assert "User Resource 1" in titles
    assert "User Resource 2" in titles

def test_get_resource_by_id(db_session):
    """Test retrieving a resource by ID."""
    resource = ResourceFactory(title="ID Test Resource")
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)

    fetched_resource = db_session.query(Resource).filter_by(id=resource.id).first()
    assert fetched_resource is not None
    assert fetched_resource.title == "ID Test Resource"

def test_update_resource_url(db_session):
    """Test updating a resource URL."""
    resource = ResourceFactory(title="URL Update Test Resource", url="http://oldurl.com")
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="URL Update Test Resource").first()
    resource_to_update.url = "http://newurl.com"
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="URL Update Test Resource").first()
    assert updated_resource.url == "http://newurl.com"

def test_count_resources(db_session):
    """Test counting total resources."""
    initial_count = db_session.query(Resource).count()

    resource1 = ResourceFactory(title="Count Test Resource 1")
    resource2 = ResourceFactory(title="Count Test Resource 2")
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.commit()

    new_count = db_session.query(Resource).count()
    assert new_count == initial_count + 2

def test_get_starred_resources(db_session):
    """Test retrieving all starred resources."""
    resource1 = ResourceFactory(title="Starred Resource 1", starred=True)
    resource2 = ResourceFactory(title="Starred Resource 2", starred=False)
    resource3 = ResourceFactory(title="Starred Resource 3", starred=True)
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.add(resource3)
    db_session.commit()

    starred_resources = db_session.query(Resource).filter_by(starred=True).all()
    assert len(starred_resources) == 2
    titles = [res.title for res in starred_resources]
    assert "Starred Resource 1" in titles
    assert "Starred Resource 3" in titles

def test_update_resource_description(db_session):
    """Test updating a resource description."""
    resource = ResourceFactory(title="Description Update Test Resource", description="Old Description")
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Description Update Test Resource").first()
    resource_to_update.description = "New Description"
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(title="Description Update Test Resource").first()
    assert updated_resource.description == "New Description"

def test_update_resource_title(db_session):
    """Test updating a resource title."""
    resource = ResourceFactory(title="Old Title")
    db_session.add(resource)
    db_session.commit()

    resource_to_update = db_session.query(Resource).filter_by(title="Old Title").first()
    resource_to_update.title = "New Title"
    db_session.commit()

    updated_resource = db_session.query(Resource).filter_by(id=resource.id).first()
    assert updated_resource.title == "New Title"

def test_get_resources_by_tag(db_session):
    """Test retrieving resources by a specific tag."""
    resource1 = ResourceFactory(title="Tag Search Resource 1", tags="common, unique1")
    resource2 = ResourceFactory(title="Tag Search Resource 2", tags="common, unique2")
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.commit()

    common_tag_resources = db_session.query(Resource).filter(Resource.tags.contains("common")).all()
    assert len(common_tag_resources) == 2
    titles = [res.title for res in common_tag_resources]
    assert "Tag Search Resource 1" in titles
    assert "Tag Search Resource 2" in titles

def test_get_unread_resources(db_session):
    """Test retrieving all unread resources."""
    resource1 = ResourceFactory(title="Unread Resource 1", read_status=False)
    resource2 = ResourceFactory(title="Read Resource", read_status=True)
    resource3 = ResourceFactory(title="Unread Resource 2", read_status=False)
    db_session.add(resource1)
    db_session.add(resource2)
    db_session.add(resource3)
    db_session.commit()

    unread_resources = db_session.query(Resource).filter_by(read_status=False).all()
    assert len(unread_resources) == 2
    titles = [res.title for res in unread_resources]
    assert "Unread Resource 1" in titles
    assert "Unread Resource 2" in titles
    assert "Read Resource" not in titles