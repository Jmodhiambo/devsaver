#!/usr/bin/env python3
"""Schema definitions for resource-related data."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.utils.pydantic.schema import as_form

@as_form
class ResourceBase(BaseModel):
    """Base schema for resource data."""
    title: str
    description: Optional[str] = None
    tags: Optional[str] = None
    type: str
    url: Optional[str] = None
    source: str
    read_status: bool = False
    starred: bool = False
    user_id: int

@as_form
class ResourceCreate(ResourceBase):
    """Schema for creating a new resource."""
    pass

@as_form
class ResourceUpdate(BaseModel):
    """Schema for updating resource information."""
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    read_status: Optional[bool] = None
    starred: Optional[bool] = None

@as_form
class ResourceInDBBase(ResourceBase):
    """Base schema for resource data stored in the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@as_form
class Resource(ResourceInDBBase):
    """Schema for resource data returned to clients."""
    pass

@as_form
class ResourcePublic(BaseModel):
    """Schema for public resource data."""
    id: int
    title: str
    description: Optional[str] = None
    tags: Optional[str] = None
    type: str
    url: Optional[str] = None
    source: str
    created_at: datetime
    updated_at: datetime
    read_status: bool
    starred: bool

    class Config:
        from_attributes = True

@as_form
class ResourceList(BaseModel):
    """Schema for a list of resources."""
    resources: list[ResourcePublic]
    total: int
    page: int
    size: int

    class Config:
        from_attributes = True

@as_form
class ResourceStats(BaseModel):
    """Schema for resource statistics."""
    total_resources: int
    read_resources: int
    unread_resources: int
    starred_resources: int

    class Config:
        from_attributes = True

@as_form
class ResourceFilter(BaseModel):
    """Schema for filtering resources."""
    type: Optional[str] = None
    tags: Optional[str] = None
    read_status: Optional[bool] = False
    starred: Optional[bool] = False
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

@as_form
class ResourceBulkUpdate(BaseModel):
    """Schema for bulk updating resources."""
    resource_ids: list[int]
    read_status: Optional[bool] = None
    starred: Optional[bool] = None

    class Config:
        from_attributes = True

@as_form
class ResourceBulkDelete(BaseModel):
    """Schema for bulk deleting resources."""
    resource_ids: list[int]

    class Config:
        from_attributes = True

@as_form
class ResourceSearch(BaseModel):
    """Schema for searching resources."""
    query: str
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

@as_form
class ResourceImport(BaseModel):
    """Schema for importing resources."""
    resources: list[ResourceCreate]

    class Config:
        from_attributes = True
        

@as_form
class ResourceExport(BaseModel):
    """Schema for exporting resources."""
    resource_ids: Optional[list[int]] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

@as_form
class ResourceCountByType(BaseModel):
    """Schema for counting resources by type."""
    type: str
    count: int

    class Config:
        from_attributes = True

@as_form
class ResourceCountByTag(BaseModel):
    """Schema for counting resources by tag."""
    tag: str
    count: int

    class Config:
        from_attributes = True