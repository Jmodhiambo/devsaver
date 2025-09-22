#!/usr/bin/env python3
"""Custom exceptions for the DevSaver application."""
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException # This catches and fastapi.HTTPException raises
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="app/templates")

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    # Redirect to login if 401 status code
    if exc.status_code == 401:
        return RedirectResponse("/login", status_code=303)
    
    # Render templates for other status codes or errors
    template_name = f"errors/{exc.status_code}.html"
    try:
        return templates.TemplateResponse(
            template_name, 
            {"request": request, "status_code":exc.status_code, "detail": exc.detail}
        )
    except Exception:
        return templates.TemplateResponse(
            "errors/generic.html", 
            {"request": request, "status_code":exc.status_code, "detail": exc.detail}
        )