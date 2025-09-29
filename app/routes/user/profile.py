#!/usr/bin/env python3
"""User update route."""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.schemas.user import UserUpdate
from app.services.user_services import update_user_profile, get_user_by_id
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates

router = APIRouter()

@router.get("/profile/")
async def profile(request: Request, session_user: Optional[str] = Depends(check_current_user)) -> HTMLResponse:
    """Render the profile page."""
    if not session_user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    
    msg = request.query_params.get("msg")
    if msg:
        msg = "Profile updated successfully!"

    user_id = request.session.get("user")
    user = get_user_by_id(user_id)
    return templates.TemplateResponse("pages/profile.html", {"request": request, "title": "Profile Update", "errors": {}, "data": user, "msg": msg})

@router.post("/profile/")
async def update_profile(request: Request, form: UserUpdate = Depends(UserUpdate.as_form)) -> RedirectResponse:
    """Handle user profile update. Just fullname update for now"""
    request.state.template = "pages/profile.html"

    user_id = request.session.get("user")
    if form.fullname == "":
        form.fullname = None

    success = update_user_profile(user_id, fullname=form.fullname)
    if not success:
        # Triggers ValueError → handled by global handler
        raise ValueError("Profile update failed. Please try again!")

    return RedirectResponse("/profile?msg=updated", status_code=303)