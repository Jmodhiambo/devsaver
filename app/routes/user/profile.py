#!/usr/bin/env python3
"""User update route."""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.schemas.user import UserUpdate, User as UserSchema
from app.services.user_services import update_user_service
from app.utils.auth.loggin import check_current_user
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

