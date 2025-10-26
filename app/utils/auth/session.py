#!/usr/bin/env python3
"""Utility functions for user authentication and login."""

from fastapi import Request

def check_current_user(request: Request):
    """Retrieve the current logged-in user from the session."""
    user = request.session.get("user")

    return user