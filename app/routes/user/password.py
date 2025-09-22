#!/usr/bin/env python3
"""Handle password updates"""

from app.services.user_services import update_user_profile, get_user_by_email_service
from fastapi import Request, Depends, Form, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from app.utils.auth.loggin import check_current_user
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/forgot-password")
async def forgot_password_page(request: Request):
    """Render the forgot password page."""
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("forgot_password.html", {"request": request, "title": "Forgot Password", "msg": msg})

@router.post("/forgot_password")
async def forgot_password_action(request: Request, email: str = Form(...)):
    """Handle forgot password action."""
    # await send_password_request(email)
    user = get_user_by_email_service(email)
    if not user:
        raise RedirectResponse("/forgot-password?msg=email_not_found", status_code=303)    
    return RedirectResponse("/reset-password?email={email}", status_code=303)

@router.get("/reset-password")
async def reset_password_page(request: Request):
    """Render the reset password page."""
    msg = request.query_params.get("msg")
    email = request.query_params.get("email")
    return templates.TemplateResponse("reset_password.html", {"request": request, "title": "Reset Password", "msg": msg, "email": email})

@router.post("/reset-password")
async def reset_password_action(request: Request, email: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...)):
    """Handle reset password action."""
    if new_password != confirm_password:
        return templates.TemplateResponse("reset_password.html", {"request": request, "title": "Reset Password", "email": email, "msg": "password_mismatch"})
    user = get_user_by_email_service(email)
    update_user_profile(user["id"], password=new_password)

    return RedirectResponse("/login?msg=password_reset", status_code=303)    