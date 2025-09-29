#!/usr/bin/env python3
""" User registration route."""

from app.schemas.user import UserCreate
from app.services.user_services import register_user
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates

router = APIRouter()

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the registration page."""
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("pages/register.html", {"request": request, "title": "Register", "msg": msg, "data": {}, "errors": {}})

@router.post("/register")
async def register_action(request: Request, form: UserCreate = Depends(UserCreate.as_form)): # fullname: Optional[str] = Form(None), username: str = Form(...), email: str = Form(...), password: str = Form(...)
    """Handle user registration with reusable error handling."""
    request.state.template = "pages/register.html"  # Tell the ValueError exception handler to use this template

    user = register_user(form.username, form.email.lower(), form.password, form.fullname)
    if user:
        return RedirectResponse("/login?msg=registered", status_code=303)
    
    # Triggers ValueError → handled by global handler
    raise ValueError("Registration failed. Please try again!")