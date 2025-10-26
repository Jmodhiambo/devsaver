#!/usr/bin/env python3
"""User update route."""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.schemas.user import UserUpdate, PasswordChange
from app.services.user_services import update_user_profile, get_user_by_id, authenticate_user, get_user_profile, update_user_password
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates
from app.core.logging_config import logger

router = APIRouter()

@router.get("/profile/")
async def profile(request: Request, session_user: Optional[str] = Depends(check_current_user)) -> HTMLResponse:
    """Render the profile page."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    msg = request.query_params.get("msg")
    if msg == "updated":
        msg = "Profile updated successfully!"

    user_id = request.session.get("user")
    user = get_user_by_id(user_id)
    return templates.TemplateResponse(
        "pages/profile.html",
        {"request": request, "title": "Profile Update", "errors": {}, "user": session_user, "data": user, "msg": msg}
    )

@router.post("/profile/")
async def update_profile(request: Request, form: UserUpdate = Depends(UserUpdate.as_form), session_user: Optional[str] = Depends(check_current_user)) -> RedirectResponse:
    """Handle user profile update. Just fullname update for now"""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    request.state.template = "pages/profile.html"

    user_id = request.session.get("user")
    print("Session exists:", "session" in request.scope)


    if form.fullname == "":
        form.fullname = None  

    success = update_user_profile(user_id, fullname=form.fullname)
    if not success:
        # Triggers ValueError → handled by global handler
        logger.error("Profile update failed. Please try again!")
        raise ValueError("Profile update failed. Please try again!")
    
    logger.info(f"User ID {user_id} updated their profile successfully.")
    return RedirectResponse("/profile?msg=updated", status_code=303)

@router.get("/profile/change-password", response_class=HTMLResponse)
async def change_password_get(request: Request, session_user: Optional[str] = Depends(check_current_user)) -> HTMLResponse:
    """Render the change password page."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    msg = request.query_params.get("msg")
    if msg == "password_changed":
        msg = "Password changed successfully!"

    return templates.TemplateResponse(
        "pages/change_password.html",
        {"request": request, "title": "Change Password", "errors": {},"user": session_user, "data": {}, "msg": msg}
    )

@router.post("/profile/change-password", response_class=HTMLResponse)
async def change_password_post(
    request: Request, form: PasswordChange = Depends(PasswordChange.as_form), session_user: Optional[str] = Depends(check_current_user)
) -> HTMLResponse:
    """Handle password change with reusable error handling."""
    if not session_user:
        logger.error("Unauthorized Access!")
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    request.state.template = "pages/change_password.html"
    
    if form.new_password != form.confirm_password:
        logger.error("New password and confirm password do not match.")
        raise ValueError("New password and confirm password do not match.")
    
    user_id = request.session.get("user")
    user = get_user_profile(user_id)

    if not user or not authenticate_user(user.username, form.old_password):
        logger.error("Old password is incorrect.")
        raise ValueError("Old password is incorrect.")

    success = update_user_password(user_id, password=form.new_password)
    if not success:
        logger.error("Password change failed.")
        raise ValueError("Password change failed. Please ensure your old password is correct.")

    logger.info(f"User ID {user_id} changed their password successfully.")
    return RedirectResponse("/dashboard?msg=password_changed", status_code=303)