#!/usr/bin/env python3
"""Dashboard page route."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.auth.loggin import check_current_user
from typing import Optional


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the home page."""
    if not user:
        return HTMLResponse("Unauthorized Access!", status_code=401)
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Welcome to the DevSaver App"})