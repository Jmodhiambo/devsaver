#!/usr/bin/env python3
"""Home page route."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("home.html", {"request": request, "title": "Welcome Home"})