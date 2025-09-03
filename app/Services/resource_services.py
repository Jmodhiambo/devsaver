#!/usr/bin/env python3
"""Service layer for resource-related operations."""

from app.models.resource import Resource
from typing import List, Optional
from app.models.user_crud import get_user_by_id
import app.models.resource_crud as resource_crud
"""from app.models.resource_crud import (
    create_resource, get_resource_by_id, update_resource,
    delete_resource, get_resources_by_user, get_all_resources,
    get_resources_by_type, get_resources_by_tag, get_starred_resources,
    get_unread_resources, get_resources_by_source, mark_resource_as_read,
    toggle_star_resource, search_resources, get_recent_resources,
    get_resources_by_date_range, delete_resources_by_user, count_resources_by_source,
    count_resources_by_tag, count_resources_by_type, count_starred_resources_by_user,
    count_unread_resources_by_user, bulk_delete_resources, bulk_update_resources,
    get_distinct_sources_by_user, get_most_common_tags, get_most_common_types,
    get_resources_paginated, get_distinct_tags_by_user, get_distinct_types_by_user,
)"""
def add_resource(
        title: str,
        type: str,
        source: str,
        user_id: int,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        url: Optional[str] = None,
) -> dict:
    """Add a new resource."""
    if not resource_crud.get_user_by_id(user_id):
        raise ValueError("User does not exist")
    
    return resource_crud.create_resource(
        title=title, description=description, tags=tags, type=type, url=url, source=source, user_id=user_id
    )

def get_resource(resource_id: int) -> Optional[Resource]:
    """Get a resource by its ID."""
    return resource_crud.get_resource_by_id(resource_id)

def update_resource_details(resource_id: int, **kwargs) -> Optional[Resource]:
    """Update resource details."""
    if not resource_crud.get_resource_by_id(resource_id):
        raise ValueError("Resource does not exist.")
    return resource_crud.update_resource(resource_id, **kwargs)

def remove_resource(resource_id: int) -> bool:
    """Remove a resource by its ID."""
    if not resource_crud.get_resource_by_id(resource_id):
        raise ValueError("Resource does not exist.")
    return resource_crud.delete_resource(resource_id)

def list_all_resources() -> List[dict]:
    """List all resources."""
    return resource_crud.get_all_resources()

def list_resources_by_user(user_id: int) -> List[Resource]:
    """List resources by a specific user."""
    if not resource_crud.get_user_by_id(user_id):
        raise ValueError("User does not exist")
    return resource_crud.get_resources_by_user(user_id)

def list_resources_by_type(user_id: int, resource_type: str) -> List[Resource]:
    """List resources by type."""
    return resource_crud.get_resources_by_type(user_id, resource_type)

def list_resources_by_tag(user_id: int, tag: str) -> List[Resource]:
    """List resources by tag."""
    return resource_crud.get_resources_by_tag(user_id, tag)