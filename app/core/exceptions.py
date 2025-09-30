#!/usr/bin/env python3
"""Custom exceptions for the DevSaver application."""
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException # This catches and fastapi.HTTPException raises
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse, HTMLResponse
from app.core.templates import templates
from app.utils.pydantic.validation_error import validation_path, normalize_errors
# from jinja2 import TemplateError
# from pydantic import ValidationError

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    # Redirect to login if 401 status code
    if exc.status_code == 401:
        return RedirectResponse("/login?msg=unauthorized", status_code=303)
    
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
    
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> HTMLResponse:
    """Handle Pydantic/FastAPI form validation errors."""
    errors = normalize_errors(exc.errors())
    template, title = validation_path(request)
    form_data = await request.form()

    return templates.TemplateResponse(
        template,
        {"request": request, "title": title, "errors": errors, "data": form_data},
        status_code=400
    )

async def value_error_exception_handler(request: Request, exc: ValueError) -> HTMLResponse:
    """Handle Pydantic/FastAPI value errors."""
    template = getattr(request.state, "template", "pages/error.html")
    form_data = await request.form()

    return templates.TemplateResponse(
        template, 
        {"request": request, "title": "Value Error", "errors": {"general": str(exc)}, "data": form_data}, 
        status_code=400
    )

# async def template_exception_handler(request: Request, exc: TemplateError) -> HTMLResponse:
#     """Handle Jinja2 template errors."""
#     # Log the real error for debugging
#     print(f"Template rendering failed: {exc}")

#     return templates.TemplateResponse(
#         "errors/500.html", 
#         {"request": request}, 
#         status_code=400
#     )