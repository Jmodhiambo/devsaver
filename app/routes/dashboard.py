#!/usr/bin/env python3
"""Dashboard page route."""

from fastapi import APIRouter, Request, Depends, HTTPException
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates


router = APIRouter()

@router.get("/dashboard")
async def dashboard(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the home page."""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    return templates.TemplateResponse("pages/dashboard.html", {"request": request, "title": "Welcome to the DevSaver App"})