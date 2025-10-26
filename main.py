#!/usr/bin/env python3
"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import home, auth, dashboard, admin
from app.routes.user import reset_password, user, register, profile
from app.routes.resource import rss, resources
from app.core.config import SESSION_SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
import app.core.exceptions as e
from app.core.logging_middleware import  ContextualASGIMiddleware #ContextualLoggingMiddleware,
from app.core.logging_config import logger
from app.core.db_init import init_db_tables
from app.core.database import engine


app = FastAPI(title="DevSaver", description="A tool to save and manage development resources.")

# Middlewares
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
app.add_middleware(ContextualASGIMiddleware)
# app.add_middleware(ContextualLoggingMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Static uploads directory
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Include User routers
app.include_router(home.router, tags=["home"])
app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(dashboard.router, tags=["dashboard"])
app.include_router(register.router, tags=["register"])
app.include_router(reset_password.router, tags=["password"])
app.include_router(profile.router, tags=["profile"])
app.include_router(admin.router, tags=["admin"])

# Include Resource routers
app.include_router(rss.router, tags=["rss"])
app.include_router(resources.router, tags=["resources"])

# Auto-create DB tables on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up DevSaver...")
    init_db_tables()  # Create DB tables if they don't exist

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Closing database connections...")
    engine.dispose()
    logger.info("DevSaver application shut down cleanly.")

# Register handlers globally
app.add_exception_handler(StarletteHTTPException, e.http_exception_handler)
app.add_exception_handler(RequestValidationError, e.validation_exception_handler)
app.add_exception_handler(ValueError, e.value_error_exception_handler)