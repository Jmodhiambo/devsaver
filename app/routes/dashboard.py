#!/usr/bin/env python3
"""Dashboard page route (refactored to use GET filters)."""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from app.utils.auth.session import check_current_user
from app.core.templates import templates
from app.services.resource_services import (
    get_resource_by_id_service,
    list_resources_by_user,
    list_resources_by_type,
    list_resources_by_tag,
)

router = APIRouter()


@router.get("/dashboard", name="dashboard")
async def dashboard(
    request: Request,
    session_user: Optional[str] = Depends(check_current_user),
    filter: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Render the dashboard with optional filtering by type or tags."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")

    user_id = request.session.get("user")
    msg = request.query_params.get("msg")
    if msg == "uploaded":
        msg = "Resource uploaded successfully!"
    if msg == "updated":
        msg = "Resource updated successfully!"
    if msg == "no-change":
        msg = "No changes detected."
    if msg == "password_changed":
        msg = "Password changed successfully!"

    resources = []

    # Tag-based search takes priority
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        found = []
        for tag in tag_list:
            tag_resources = list_resources_by_tag(user_id, tag)
            for r in tag_resources:
                if r not in found:
                    found.append(r)
        resources = found
        active_type = "Tag"

    # Otherwise, filter by resource type
    elif filter and filter.lower() != "all":
        resources = list_resources_by_type(user_id, filter.capitalize())
        active_type = filter.capitalize()

    # Otherwise, show all resources
    else:
        resources = list_resources_by_user(user_id)
        active_type = "All"

    return templates.TemplateResponse(
        "pages/dashboard.html",
        {
            "request": request,
            "title": "Welcome to the DevSaver App",
            "resources": resources,
            "user": session_user,
            "msg": msg,
            "type": active_type,
        },
)

@router.get("/dashboard/{resource_id}/preview", response_class=HTMLResponse)
async def resource_preview(request: Request, resource_id: int, session_user: Optional[str] = Depends(check_current_user)):
    """Render the resource preview page."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")

    resource = get_resource_by_id_service(resource_id)
    if not resource:
        return HTMLResponse("<p>Resource not found!</p>", status_code=404)
    
    return templates.TemplateResponse(
        "partials/resource_preview.html",
        {"request": request, "resource": resource}
    )

@router.get("/dashboard/{resource_id}/view", response_class=HTMLResponse)
async def resource_view(request: Request, resource_id: int, session_user: Optional[str] = Depends(check_current_user)):
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    resource = get_resource_by_id_service(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return templates.TemplateResponse(
        "pages/resource_view.html",
        {"request": request, "resource": resource, "user": session_user}
    )
