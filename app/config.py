#!/usr/bin/env python3
"""Configuration settings for the FastAPI application."""

from starlette.config import Config

config = Config(".env")

SESSION_SECRET_KEY: str = config("SESSION_SECRET_KEY", cast=str, default="devsaver-session-key")