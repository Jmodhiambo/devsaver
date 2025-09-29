#!/usr/bin/env python3
"""Admin routes for DevSaver."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.utils.auth.session import check_current_user
from app.core.templates import templates
from app.services.user_services import list_all_users, remove_user

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

@router.get("/admin/delete-user/{user_id}", response_class=HTMLResponse)
async def delete_user(request: Request, user_id: int, user: str = Depends(check_current_user)) -> RedirectResponse:
    """Handle user deletion (admin only)."""
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    remove_user(user_id)

    return RedirectResponse("/admin?msg=user_deleted", status_code=303)