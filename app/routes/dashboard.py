#!/usr/bin/env python3
"""Dashboard page route."""

from fastapi import APIRouter, Request, Depends, HTTPException
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates
from app.services.resource_services import list_resources_by_user


router = APIRouter()

@router.get("/dashboard")
async def dashboard(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the home page."""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    msg = request.query_params.get("msg")
    
    user_id = request.session.get("user")
    resources = list_resources_by_user(user_id)
    return templates.TemplateResponse("pages/dashboard.html", {"request": request, "title": "Welcome to the DevSaver App", "resources": resources, "msg": msg})