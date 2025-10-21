#!/usr/bin/env python3
"""Resources API routes."""

import os
from fastapi import APIRouter, Request, HTTPException, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.services.resource_services import (
    add_resource, remove_resource, list_resources_by_user, get_resource_by_id_service, update_resource_details, get_resource_by_original_filename_service)
from app.utils.auth.session import check_current_user
from app.core.templates import templates
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "app/uploads/"

# Make sure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/resources/upload", response_class=HTMLResponse)
def resource_upload(request: Request, session_user: str = Depends(check_current_user)) -> HTMLResponse:
    """Render the resources uploads page."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    return templates.TemplateResponse("pages/upload_resource.html", {"request": request, "title": "Upload Resource", "user": session_user, "data": {}, "errors": {}})

@router.post("/resources/upload", response_class=HTMLResponse)
async def handle_resource_upload(request: Request, form: ResourceCreate = Depends(ResourceCreate.as_form), file: UploadFile = File(None), session_user: str = Depends(check_current_user)) -> HTMLResponse:
    """Handle resource upload form submission."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    user_id = request.session.get("user")
    
    if file.filename and get_resource_by_original_filename_service(user_id, file.filename):
        return RedirectResponse(url="/dashboard?msg=A resource with the same filename already exists.", status_code=303)

    request.state.template = "pages/upload_resource.html"

    if file and not form.external_url: # File upload is optional, so checks if file:
        # Generate a unique filename to avoid collisions
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"devsaver-{uuid4().hex}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        external_url = f"/uploads/{unique_filename}"
        original_filename = file.filename
    else:
        external_url = form.external_url
        original_filename = None
    
    success = add_resource(
        title=form.title, type=form.type, source=form.source, user_id=user_id, description=form.description, tags=form.tags, url=external_url, original_filename=original_filename
    )

    if success:
        return RedirectResponse(url="/dashboard?msg=Resource uploaded successfully!", status_code=303)
        # resources = list_resources_by_user(request.session.get("user"))
        # return templates.TemplateResponse("pages/dashboard.html", {"request": request, "title": "Dashboard", "resources": resources, "msg": "Resource uploaded successfully!"})
    
    raise ValueError("Failed to upload resource. Please try again.")

@router.post("/resources/delete-resource/{resource_id}", response_class=HTMLResponse, name="delete-resource")
def delete_resource(resource_id: int, request: Request, session_user: str = Depends(check_current_user)) -> HTMLResponse:
    """Handle resource deletion."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    remove_resource(resource_id)

    resources = list_resources_by_user(request.session.get("user"))

    return templates.TemplateResponse(
        "pages/dashboard.html", 
        {"request": request, "title": "Dashboard", "resources": resources, "user": session_user, "msg": "Resource has been successfully deleted."}
    )

@router.get("/resources/edit-resource/{resource_id}", response_class=HTMLResponse)
def edit_resource(resource_id: int, request: Request, session_user: str = Depends(check_current_user)) -> HTMLResponse:
    """Render the resource edit page."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    resource = get_resource_by_id_service(resource_id)
    if not resource:
        raise ValueError("Resource not found!")

    return templates.TemplateResponse("pages/edit_resource.html", {"request": request, "title": "Edit Resource", "resource": resource, "user": session_user, "errors": {}})

@router.post("/resources/edit-resource/{resource_id}", response_class=HTMLResponse)
async def handle_edit_resource(resource_id: int, request: Request, form: ResourceUpdate = Depends(ResourceUpdate.as_form), session_user: str = Depends(check_current_user)) -> HTMLResponse:
    """Handle resource edit form submission."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    request.state.template = "pages/edit_resource.html"
    
    user_id = request.session.get("user")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    # Verify resource exists and owned by user
    resource = get_resource_by_id_service(resource_id)
    if not resource or resource.user_id != user_id:
        raise HTTPException(status_code=404, detail="You are not authorized to edit this resource.")
    
    # Converting "" to None for optional fields
    submitted_data = {
        k: (v if v != "" else None) for k, v in form.dict().items()
    }

    # Preserving the existing URL if no new URL is provided
    if submitted_data.get("url") is None:
        submitted_data["url"] = resource.url

    # Exclude fields that should not be updated as form carries everything
    excluded_fields = {"user_id", "created_at", "read_status", "starred", "id"}

    # Remove excluded fields
    submitted_data = {k: v for k, v in submitted_data.items() if k not in excluded_fields}
    
    # Check if any field has been changed
    field_to_update = {
        k: v for k, v in submitted_data.items()
        if v is not None and v != getattr(resource, k)
    }

    if not field_to_update:
        return RedirectResponse(url="/dashboard?msg=No changes detected.", status_code=303)

    success = update_resource_details(resource_id, user_id=user_id, **field_to_update)

    if success:
        return RedirectResponse(url="/dashboard?msg=Resource updated successfully!", status_code=303)
            
    raise HTTPException(status_code=400, detail="Failed to update resource. Please try again.")