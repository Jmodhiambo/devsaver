#!/usr/bin/env python3
"""Dashboard page route."""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.utils.auth.session import check_current_user
from typing import Optional


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def dashboard(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the home page."""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Welcome to the DevSaver App"})