#!/usr/bin/env python3
"""User update route."""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from app.schemas.user import UserUpdate, User as UserSchema
from app.services.user_services import update_user_profile
from app.utils.auth.session import check_current_user
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/profile/")
async def profile(request: Request, user: Optional[str] = Depends(check_current_user)):
    """Render the profile page."""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Access!")
    return templates.TemplateResponse("profile.html", {"request": request, "title": "Profile"})