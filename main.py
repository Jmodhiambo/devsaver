#!/usr/bin/env python3
"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import home, auth, dashboard
from app.routes.user import forgot_password, user, register, profile
from app.core.config import SESSION_SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import http_exception_handler
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DevSaver", description="A tool to save and manage development resources.", version="1.0.0")

# CORS middleware configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# Session secret key for the SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(home.router, tags=["home"])
app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(dashboard.router, tags=["dashboard"])
app.include_router(register.router, tags=["register"])
app.include_router(forgot_password.router, tags=["password"])
app.include_router(profile.router, tags=["profile"])

# Register handlers globally
app.add_exception_handler(StarletteHTTPException, http_exception_handler)