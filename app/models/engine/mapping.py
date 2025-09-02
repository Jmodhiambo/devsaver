#!/usr/bin/env python3
"""Databse mapping and model registration for DevSaver."""

from app.models.engine.db import engine, Base
from app.models import resource, user  # this will register your models

Base.metadata.create_all(bind=engine)