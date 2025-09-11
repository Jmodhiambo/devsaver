#!/usr/bin/env python3
"""Main application routes."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import home, users, auth

app = FastAPI(title="DevSaver", description="A tool to save and manage development resources.", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(home.router)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])