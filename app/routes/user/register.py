#!/usr/bin/env python3
""" User registration route."""

from app.schemas.user import UserCreate
from app.services.user_services import register_user
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.utils.auth.loggin import check_current_user
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the registration page."""
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register", "msg": msg})

@router.post("/register")
async def register_action(request: Request, fullname: Optional[str] = Form(None), username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """Handle user registration."""
    user_data = UserCreate(fullname=fullname, username=username, email=email, password=password)
    user = register_user(user_data.username, user_data.email, user_data.password, user_data.fullname)
    if user:
        return RedirectResponse("/login?msg=registered", status_code=303)
    return RedirectResponse("/register?msg=error", status_code=303)