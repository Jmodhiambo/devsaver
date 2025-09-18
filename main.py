#!/usr/bin/env python3
"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import home, auth, dashboard
from app.routes.user import user, register
from app.config import SESSION_SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware

from app.routes.user import register

app = FastAPI(title="DevSaver", description="A tool to save and manage development resources.", version="1.0.0")

# Session secret key for the SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(home.router)
app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(dashboard.router, tags=["dashboard"])
app.include_router(register.router, tags=["register"])