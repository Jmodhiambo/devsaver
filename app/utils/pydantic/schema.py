#!/usr/bin/env python3
"""Pydantic form utilities."""

# app/utils/pydantic/schema.py
from typing import Any
from inspect import Signature, Parameter
from fastapi import Form

def as_form(cls):
    """
    Decorator to add an `as_form` dependency function to a Pydantic model.
    Usage:
      @as_form
      class Login(BaseModel):
          username: str
          password: str

      @router.post("/login")
      async def login(data: Login = Depends(Login.as_form)):
          ...
    Works with Pydantic v2 (and v1 fallback).
    """
    # grab fields for Pydantic v2 (model_fields) or v1 (__fields__)
    fields = getattr(cls, "model_fields", None) or getattr(cls, "__fields__", None)
    params = []

    for name, model_field in fields.items():
        # Try to get the Python type for annotation if available
        annotation = getattr(model_field, "annotation", None) or getattr(model_field, "type_", None) or Any

        # Determine whether the field is required
        is_required_attr = getattr(model_field, "is_required", None)
        if callable(is_required_attr):
            required = model_field.is_required()
        else:
            # fallback for v1 or if property exists as attribute
            required = bool(getattr(model_field, "required", False))

        # Build Form(...) default depending on whether the field is required
        if required:
            default = Form(...)
        else:
            default_value = getattr(model_field, "default", None)
            default = Form(default_value)

        # Create a keyword-only parameter for the signature
        params.append(
            Parameter(
                name,
                kind=Parameter.KEYWORD_ONLY,
                annotation=annotation,
                default=default,
            )
        )

    async def _as_form(**data):
        # instantiate the model with the parsed form data
        return cls(**data)

    # assign the created signature so FastAPI knows the parameters and their defaults
    _as_form.__signature__ = Signature(parameters=params)

    # attach the function to the class (no classmethod wrapper — the closure captures `cls`)
    setattr(cls, "as_form", _as_form)
    return cls