#!/usr/bin/env python3
"""Handle password updates"""

from app.services.user_services import get_user_by_email_service, update_user_password
from fastapi import APIRouter,Request, Form, Depends
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from app.schemas.user import PasswordResetRequest


router = APIRouter()

@router.get("/forgot-password")
async def forgot_password_page(request: Request):
    """Render the forgot password page."""
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("pages/forgot_password.html", {"request": request, "title": "Forgot Password", "msg": msg})

@router.post("/forgot-password")
async def forgot_password_action(request: Request, email: str = Form(...)):
    """Handle forgot password action."""
    # await send_password_request(email)
    user = get_user_by_email_service(email)
    if not user:
        return RedirectResponse("/forgot-password?msg=email_not_found", status_code=303)    
    return RedirectResponse(f"/reset-password?email={email}", status_code=303)

@router.get("/reset-password")
async def reset_password_page(request: Request):
    """Render the reset password page."""
    msg = request.query_params.get("msg")
    email = request.query_params.get("email")
    return templates.TemplateResponse(
        "pages/reset_password.html",
        {"request": request, "title": "Reset Password", "msg": msg, "email": email, "errors": {}, "data": {}}
    )

@router.post("/reset-password")
async def reset_password_action(request: Request, form: PasswordResetRequest = Depends(PasswordResetRequest.as_form)): #email: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...)
    """Handle reset password action."""
    request.state.template = "pages/reset_password.html"
    if form.new_password != form.confirm_password:
        raise ValueError("Passwords do not match. Please try again!")
    
    email = form.email.lower()
    user = get_user_by_email_service(email)
    success = update_user_password(user.id, password=form.new_password)
    if success:
        return RedirectResponse("/login?msg=password_reset", status_code=303)
    
    raise ValueError("Password update failed. Please try again!")