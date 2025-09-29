#!/usr/bin/env python3
"""Service layer for resource-related operations."""

from app.models.resource import Resource
from typing import List, Optional
import app.crud.resource_crud as resource_crud

def add_resource(
        title: str,
        type: str,
        source: str,
        user_id: int,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        url: Optional[str] = None,
) -> Resource:
    """Add a new resource."""
    from app.crud.user_crud import get_user_by_id
    if not get_user_by_id(user_id):
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

def list_starred_resources(user_id: int) -> List[Resource]:
    """List starred resources for a user."""
    return resource_crud.get_starred_resources(user_id)

def list_unread_resources(user_id: int) -> List[Resource]:
    """List unread resources for a user."""
    return resource_crud.get_unread_resources(user_id)

def list_resources_by_source(user_id: int, source: str) -> List[Resource]:
    """List resources by source."""
    return resource_crud.get_resources_by_source(user_id, source)

def mark_as_read(resource_id: int) -> Optional[Resource]:
    """Mark a resource as read."""
    if not resource_crud.get_resource_by_id(resource_id):
        raise ValueError("Resource does not exist.")
    return resource_crud.mark_resource_as_read(resource_id)

def toggle_star(resource_id: int) -> Optional[Resource]:
    """Toggle the star status of a resource."""
    if not resource_crud.get_resource_by_id(resource_id):
        raise ValueError("Resource does not exist.")
    return resource_crud.toggle_star_resource(resource_id)

def search_for_resources(user_id: int, query: str) -> List[Resource]:
    """Search for resources by a query string."""
    return resource_crud.search_resources(user_id, query)

def list_recent_resources(user_id: int, limit: int = 10) -> List[Resource]:
    """List recent resources for a user."""
    return resource_crud.get_recent_resources(user_id, limit)

def list_resources_by_date_range(user_id: int, start_date: str, end_date: str) -> List[Resource]:
    """List resources within a specific date range."""
    return resource_crud.get_resources_by_date_range(user_id, start_date, end_date)

def remove_resources_by_user(user_id: int) -> int:
    """Remove all resources for a specific user."""
    if not resource_crud.get_user_by_id(user_id):
        raise ValueError("User does not exist")
    return resource_crud.delete_resources_by_user(user_id)

def count_resources_by_source(user_id: int, source: str) -> int:
    """Count resources grouped by source for a user."""
    return resource_crud.count_resources_by_source(user_id, source)

def count_resources_by_tag(user_id: int, tags: str) -> int:
    """Count resources grouped by tag for a user."""
    return resource_crud.count_resources_by_tag(user_id, tags)

def count_resources_by_type(user_id: int, resource_type: str) -> int:
    """Count resources grouped by type for a user."""
    return resource_crud.count_resources_by_type(user_id, resource_type)

def count_starred_resources(user_id: int) -> int:
    """Count starred resources for a user."""
    return resource_crud.count_starred_resources_by_user(user_id)

def count_unread_resources(user_id: int) -> int:
    """Count unread resources for a user."""
    return resource_crud.count_unread_resources_by_user(user_id)

def bulk_remove_resources(resource_ids: List[int]) -> int:
    """Bulk delete resources by their IDs."""
    return resource_crud.bulk_delete_resources(resource_ids)

def bulk_update_resources(resource_ids: List[int], **kwargs) -> int:
    """Bulk update resources by their IDs."""
    return resource_crud.bulk_update_resources(resource_ids, **kwargs)

def list_distinct_sources(user_id: int) -> List[str]:
    """List distinct sources for a user."""
    return resource_crud.get_distinct_sources_by_user(user_id)

def list_most_common_tags(user_id: int, limit: int = 5) -> List[str]:
    """List the most common tags for a user."""
    return resource_crud.get_most_common_tags(user_id, limit)

def list_most_common_types(user_id: int, limit: int = 5) -> List[str]:
    """List the most common types for a user."""
    return resource_crud.get_most_common_types(user_id, limit)

def list_resources_paginated(user_id: int, page: int = 1, page_size: int = 10) -> List[Resource]:
    """List resources with pagination."""
    return resource_crud.get_resources_paginated(user_id, page, page_size)

def list_distinct_tags(user_id: int) -> List[str]:
    """List distinct tags for a user."""
    return resource_crud.get_distinct_tags_by_user(user_id)

def list_distinct_types(user_id: int) -> List[str]: 
    """List distinct types for a user."""
    return resource_crud.get_distinct_types_by_user(user_id)