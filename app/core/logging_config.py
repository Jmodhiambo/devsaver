#!/usr/bin/env python3
"""Logging configuration for DevSaver."""

import logging
import os

# Create logs directory if it doesn’t exist
LOG_DIR = "app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

class ContextFilter(logging.Filter):
    """Inject request context (like user_id, path, and method) into logs."""
    def filter(self, record):
        from app.core.logging_middleware import request_context
        
        context = request_context.get({})
        record.user_id = context.get("user_id", "-")
        record.path = context.get("path", "-")
        record.method = context.get("method", "-")
        return True

# Create and configure the main logger
logger = logging.getLogger("DevSaver")
logger.setLevel(logging.INFO)

# Console handler
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [user=%(user_id)s] [%(method)s %(path)s] %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)

# Attach filter and handler
handler.addFilter(ContextFilter())
logger.addHandler(handler)
