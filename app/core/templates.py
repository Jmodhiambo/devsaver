#!/usr/bin/env python3
"""Template constants for the FastAPI application."""

from fastapi.templating import Jinja2Templates
from datetime import datetime

templates = Jinja2Templates(directory="app/templates")

# Add global "now" functions to Jinja2 for the footer date
templates.env.globals["now"] = datetime.now

# Clear the Jinja2 cache to force recompilation for faster develpment to prevent cache issues. Remove in production.
templates.env.cache = {}