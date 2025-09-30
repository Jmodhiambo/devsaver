#!/usr/bin/env python3
"""Admin routes for DevSaver."""

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.utils.auth.session import check_current_user
from app.core.templates import templates
from app.services.user_services import list_all_users, remove_user, get_user_by_id, update_user_profile
from app.schemas.user import UserUpdate
from typing import Optional

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: str = Depends(check_current_user))-> HTMLResponse:
    """Render the admin dashboard page."""
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    msg = request.query_params.get("msg")
    if msg == "user_deleted":
        msg = "User has been successfully deleted."
    users = list_all_users()

    return templates.TemplateResponse("pages/admin.html", {"request": request, "title": "Admin Dashboard", "users": users})

@router.post("/admin/delete-user/{user_id}", response_class=HTMLResponse, name="delete-user")
async def delete_user(request: Request, user_id: int, user: str = Depends(check_current_user)) -> RedirectResponse:
    """Handle user deletion (admin only)."""
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    remove_user(user_id)

    return RedirectResponse("/admin?msg=user_deleted", status_code=303)

@router.get("/admin/edit-user/{user_id}", response_class=HTMLResponse)
async def edit_user_get(request: Request, user_id: int, user: str = Depends(check_current_user)) -> HTMLResponse:
    """Render the edit user page (admin only)."""
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    user_obj = get_user_by_id(user_id)
    return templates.TemplateResponse("pages/edit_user.html", {"request": request, "data": user_obj, "title": "Edit User", "errors": {}, "msg": ""})

@router.post("/admin/edit-user/{user_id}", response_class=HTMLResponse)
async def edit_user_post(request: Request, user_id: int, form: UserUpdate = Depends(UserUpdate.as_form), user: str = Depends(check_current_user)) -> HTMLResponse:
    """Handle user update (admin only)."""
    request.state.template = "pages/edit_user.html"

    if not user:
        return RedirectResponse("/login", status_code=303)
    
    success = update_user_profile(user_id, fullname=form.fullname)
    if not success:
        raise ValueError("User update failed. Please try again!")

    return RedirectResponse("/admin?msg=user_updated", status_code=303)