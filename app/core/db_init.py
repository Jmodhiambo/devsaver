#!/usr/bin/env python3
"""Database initialization for DevSaver."""

from app.core.database import Base, engine
from app.core.logging_config import logger
from sqlalchemy import inspect

def init_db_tables():
  """Automatically create database tables if they don't exist."""
  inspector = inspect(engine)
  existing_tables = inspector.get_table_names()

  if not existing_tables:
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized — all tables created successfully.")
  else:
    logger.info("Database tables already exist. Skipping creation.")