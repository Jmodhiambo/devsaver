#!/usr/bin/env python3
"""Home page route."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("pages/home.html", {"request": request, "title": "Welcome Home"})