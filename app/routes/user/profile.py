#!/usr/bin/env python3
"""User update route."""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from app.schemas.user import UserUpdate, User as UserSchema
from app.services.user_services import update_user_profile
from app.utils.auth.session import check_current_user
from typing import Optional
from app.core.templates import templates

router = APIRouter()

@router.get("/profile/")
async def profile(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the profile page."""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    return templates.TemplateResponse("pages/profile.html", {"request": request, "title": "Profile"})