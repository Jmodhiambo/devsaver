#!/usr/bin/env python3
"""Resources API routes."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.schemas.resource import ResourcePublic as ResourceSchema
from app.services.resource_services import get_resource, list_all_resources
from app.utils.auth.session import check_current_user

router = APIRouter()

@router.get("/rss/", response_model=list[ResourceSchema])
def list_resources(session_user: str = Depends(check_current_user)):
    """Retrieve all resources."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    resources = list_all_resources()
    if not resources:
        return JSONResponse(content={"message": "No resources found"}, status_code=404)
    return resources

@router.get("/rss/{resource_id}", response_model=ResourceSchema)
def get_resource_by_id(resource_id: int, session_user: str = Depends(check_current_user)):
    """Retrieve a resource by ID."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    resource = get_resource(resource_id)
    if not resource:
        return JSONResponse(content={"message": f"Resource with id {resource_id} not found"}, status_code=404)
    return resource