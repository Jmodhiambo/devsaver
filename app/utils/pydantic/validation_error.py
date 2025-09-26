#!/usr/bin/env python3
"""Pydantic request validation errors utilities."""
from typing import Tuple

def validation_path(request) -> Tuple[str, str]:
    """Return the template path for RequestValidationError.
    Since validation happens before the route handler, we can only rely on URL path unlike in ValueError.
    Return (template, title) for RequestValidationError based on URL path.
    """
    if request.url.path.startswith("/login"):
        return "pages/login.html", "Login Error"
    elif request.url.path.startswith("/register"):
        return "pages/register.html", "Registration Error"
    else:
        return "pages/error.html", "Validation Error"
    
def normalize_errors(errors:dict) -> dict:
    """Normalize errors to be more user-friendly."""
    nice = {}
    for err in errors:
        field = err["loc"][-1] # Get last key in location path e.g., "username", "password"
        msg = err["msg"]
        if msg == "field required":
            msg = "This field is required"
        elif msg.startswith("ensure this value has at least"):
            msg = "Password must be at least 8 characters long"
        elif msg.startswith("value is not a valid email"):
            msg = "Please enter a valid email address"
            
        nice[field] = err["msg"]
    return nice