#!/usr/bin/env python3
"""Home page route."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from typing import Optional
from app.utils.auth.session import check_current_user


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request, session_user: Optional[str] = Depends(check_current_user)):
    """Render the home page."""
    return templates.TemplateResponse("pages/home.html", {"request": request, "title": "Welcome Home", "user": session_user})