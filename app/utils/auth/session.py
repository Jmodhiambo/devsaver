#!/usr/bin/env python3
"""Utility functions for user authentication and login."""

from fastapi import Request

def check_current_user(request: Request):
    """Retrieve the current logged-in user from the session."""
    user = request.session.get("user")

    return user

# def require_login(request: Request):
#     user = request.session.get("user")
#     expires_at = request.session.get("expires_at")

#     if not user or not expires_at:
#         return None

#     if expires_at < time.time():
#         # Session expired
#         request.session.clear()
#         return None

#     return user


# import time

# # On login
# request.session["user"] = username
# request.session["expires_at"] = time.time() + 3600  # 1 hour