#!/usr/bin/env python3
""" The App's authentication routes."""

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.user_services import authenticate_user
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the login page."""
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("pages/login.html", {"request": request, "title": "Login", "msg": msg})

@router.post("/login")
async def login_action(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handle login action."""
    request.state.template = "pages/login.html"

    user = authenticate_user(username, password)
    if not user:
        # Triggers ValueError → handled by global handler
        raise ValueError("Invalid username or password")

    request.session["user"] = user["username"]
    return RedirectResponse("/dashboard", status_code=303)

@router.get("/logout")
async def logout_action(request: Request):
    """Handle logout action."""
    request.session.pop("user", None) # request.session.clear()
    return RedirectResponse("/login?msg=logged_out", status_code=303)