#!/usr/bin/env python3
"""CRUD operations for DevSaver."""

from app.models.engine.db import get_session
from app.models.resource import Resource
from typing import List
 
def create_resource(title: str, description: str, tags: str, type: str, url:str, source: str, user_id: int) -> Resource:
    """Create a new resource in the database."""
    with get_session() as session:
        new_resource = Resource(
            title=title,
            description=description,
            tags=tags,
            type=type,
            source=source,
            url=url,
            user_id=user_id
        )
        session.add(new_resource)
        session.flush() # forces INSERT so id is assigned
        session.refresh(new_resource) # reloads from db

        return new_resource.to_dict()
    
def get_resources_by_user(user_id: int) -> List[Resource]:
    """Retrieve all resources for a given user."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id).all()
        for resource in resources:
            session.refresh(resource)
        return [res.to_dict() for res in resources]
    
def update_resource(resource_id: int, **kwargs) -> Resource | None:
    """Update an existing resource."""
    with get_session() as session:
        resource = session.query(Resource).filter(Resource.id == resource_id).first()
        if resource:
            for key, value in kwargs.items():
                setattr(resource, key, value)
            session.add(resource)
            session.flush()           # forces INSERT so id is assigned
            session.refresh(resource) # reloads from db
            return resource.to_dict()
        return None
    
def delete_resource(resource_id: int) -> bool:
    """Delete a resource from the database."""
    with get_session() as session:
        resource = session.query(Resource).filter(Resource.id == resource_id).first()
        if resource:
            session.delete(resource)
            return True
        return False
    
def get_resource_by_id(resource_id: int) -> Resource | None:
    """Retrieve a resource by its ID."""
    with get_session() as session:
        resource = session.query(Resource).filter(Resource.id == resource_id).first()
        return resource.to_dict() if resource else None
    
def get_resources_by_tag(user_id: int, tag: str) -> List[Resource]:
    """Retrieve resources for a user filtered by a specific tag."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id, Resource.tags.contains(tag)).all()
        return [res.to_dict() for res in resources]
    
def get_resources_by_type(user_id: int, resource_type: str) -> List[Resource]:
    """Retrieve resources for a user filtered by a specific type."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id, Resource.type == resource_type).all()
        return [res.to_dict() for res in resources]
    
def get_starred_resources(user_id: int) -> List[Resource]:
    """Retrieve all starred resources for a given user."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id, Resource.starred == True).all()
        return [res.to_dict() for res in resources]
    
def get_unread_resources(user_id: int) -> List[Resource]:
    """Retrieve all unread resources for a given user."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id, Resource.read_status == False).all()
        return [res.to_dict() for res in resources]
    
def mark_resource_as_read(resource_id: int) -> Resource | None:
    """Mark a resource as read."""
    with get_session() as session:
        resource = session.query(Resource).filter(Resource.id == resource_id).first()
        if resource:
            resource.read_status = True
            session.add(resource)
            return resource.to_dict()
        return None
    
def toggle_star_resource(resource_id: int) -> Resource | None:
    """Toggle the starred status of a resource."""
    with get_session() as session:
        resource = session.query(Resource).filter(Resource.id == resource_id).first()
        if resource:
            resource.starred = not resource.starred
            session.add(resource)
            return resource.to_dict()
        return None
    
def search_resources(user_id: int, query: str) -> List[Resource]:
    """Search resources for a user by title or description."""
    with get_session() as session:
        resources = session.query(Resource).filter(
            Resource.user_id == user_id,
            (Resource.title.contains(query) | Resource.description.contains(query))
        ).all()
        return [res.to_dict() for res in resources]
    
def get_recent_resources(user_id: int, limit: int = 10) -> List[Resource]:
    """Retrieve the most recent resources for a given user."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id).order_by(Resource.created_at.desc()).limit(limit).all()
        return [res.to_dict() for res in resources]
    
def get_resources_by_date_range(user_id: int, start_date: str, end_date: str) -> List[Resource]:
    """Retrieve resources for a user within a specific date range."""
    with get_session() as session:
        resources = session.query(Resource).filter(
            Resource.user_id == user_id,
            Resource.created_at >= start_date,
            Resource.created_at <= end_date
        ).all()
        return [res.to_dict() for res in resources]
    
def get_resources_by_source(user_id: int, source: str) -> List[Resource]:   
    """Retrieve resources for a user filtered by a specific source."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id, Resource.source == source).all()
        return [res.to_dict() for res in resources]
    
def get_all_resources() -> List[Resource]:
    """Retrieve all resources in the database."""
    with get_session() as session:
        resources = session.query(Resource).all()
        return [res.to_dict() for res in resources]
    
def delete_resources_by_user(user_id: int) -> int:
    """Delete all resources for a given user. Returns the number of deleted resources."""
    with get_session() as session:
        deleted_count = session.query(Resource).filter(Resource.user_id == user_id).delete()
        return deleted_count
    
def count_resources_by_user(user_id: int) -> int:
    """Count the number of resources for a given user."""
    with get_session() as session:
        return session.query(Resource).filter(Resource.user_id == user_id).count()
    
def count_starred_resources_by_user(user_id: int) -> int:
    """Count the number of starred resources for a given user."""
    with get_session() as session:
        return session.query(Resource).filter(Resource.user_id == user_id, Resource.starred == True).count()
    
def count_unread_resources_by_user(user_id: int) -> int:
    """Count the number of unread resources for a given user."""
    with get_session() as session:
        return session.query(Resource).filter(Resource.user_id == user_id, Resource.read_status == False).count()
    
def get_distinct_tags_by_user(user_id: int) -> List[str]:
    """Retrieve a list of distinct tags used by a given user."""
    with get_session() as session:
        tags = session.query(Resource.tags).filter(Resource.user_id == user_id).all()
        distinct_tags = set()
        for tag_list in tags:
            if tag_list[0]:  # Ensure the tag string is not None or empty
                for tag in tag_list[0].split(','):
                    distinct_tags.add(tag.strip())
        return list(distinct_tags)
    
def get_distinct_types_by_user(user_id: int) -> List[str]:
    """Retrieve a list of distinct resource types used by a given user."""
    with get_session() as session:
        types = session.query(Resource.type).filter(Resource.user_id == user_id).distinct().all()
        return [type_tuple[0] for type_tuple in types if type_tuple[0]]
    
def get_distinct_sources_by_user(user_id: int) -> List[str]:
    """Retrieve a list of distinct sources used by a given user."""
    with get_session() as session:
        sources = session.query(Resource.source).filter(Resource.user_id == user_id).distinct().all()
        return [source_tuple[0] for source_tuple in sources if source_tuple[0]] 
    
def bulk_update_resources(resource_ids: List[int], **kwargs) -> int:
    """Bulk update multiple resources. Returns the number of updated resources."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.id.in_(resource_ids)).all()
        for resource in resources:
            for key, value in kwargs.items():
                setattr(resource, key, value)
            session.add(resource)
        return len(resources)
    
def bulk_delete_resources(resource_ids: List[int]) -> int:
    """Bulk delete multiple resources. Returns the number of deleted resources."""
    with get_session() as session:
        deleted_count = session.query(Resource).filter(Resource.id.in_(resource_ids)).delete(synchronize_session='fetch')
        return deleted_count
    
def get_resources_paginated(user_id: int, page: int = 1, page_size: int = 10) -> List[Resource]:
    """Retrieve resources for a user with pagination."""
    with get_session() as session:
        resources = session.query(Resource).filter(Resource.user_id == user_id).offset((page - 1) * page_size).limit(page_size).all()
        return [res.to_dict() for res in resources]
    
def count_resources_by_tag(user_id: int, tag: str) -> int:
    """Count the number of resources for a user filtered by a specific tag."""
    with get_session() as session:
        return session.query(Resource).filter(Resource.user_id == user_id, Resource.tags.contains(tag)).count()
    
def count_resources_by_type(user_id: int, resource_type: str) -> int:
    """Count the number of resources for a user filtered by a specific type."""
    with get_session() as session:
        return session.query(Resource).filter(Resource.user_id == user_id, Resource.type == resource_type).count()
    
def count_resources_by_source(user_id: int, source: str) -> int:
    """Count the number of resources for a user filtered by a specific source."""
    with get_session() as session:
        return session.query(Resource).filter(Resource.user_id == user_id, Resource.source == source).count()
    
def get_most_common_tags(user_id: int, limit: int = 10) -> List[str]:
    """Retrieve the most common tags used by a given user."""
    with get_session() as session:
        tags = session.query(Resource.tags).filter(Resource.user_id == user_id).all()
        tag_count = {}
        for tag_list in tags:
            if tag_list[0]:  # Ensure the tag string is not None or empty
                for tag in tag_list[0].split(','):
                    tag = tag.strip()
                    if tag:
                        tag_count[tag] = tag_count.get(tag, 0) + 1
        sorted_tags = sorted(tag_count.items(), key=lambda item: item[1], reverse=True)
        return [tag for tag, count in sorted_tags[:limit]]
    

def get_most_common_types(user_id: int, limit: int = 10) -> List[str]:
    """Retrieve the most common resource types used by a given user."""
    with get_session() as session:
        types = session.query(Resource.type).filter(Resource.user_id == user_id).all()
        type_count = {}
        for type_tuple in types:
            type_value = type_tuple[0]
            if type_value:
                type_count[type_value] = type_count.get(type_value, 0) + 1
        sorted_types = sorted(type_count.items(), key=lambda item: item[1], reverse=True)
        return [type_value for type_value, count in sorted_types[:limit]]
    
    def url_exists(url: str) -> bool | None:
        """Check if a resource with the given URL already exists."""
        with get_session() as session:
            resource = session.query(Resource).filter(Resource.url == url).first()
            return resource.to_dict() if resource else None