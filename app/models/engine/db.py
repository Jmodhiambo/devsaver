#!/usr/bin/env python3
"""Database connection and session management for DevSaver."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from collections.abc import Generator
# import os
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./devsaver.db"
# DEBUG = os.getenv("DEVSAVER_DEBUG", "0") == "1" # The equation results in False or True based on the environment variable

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False
)

# Defininng base as a subclass of DeclarativeBase
class Base(DeclarativeBase):
    """Base class for all models in DevSaver."""
    pass

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager for database session.
    With it I do not have to worry about closing the session manually or leaking sessions.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit() # Commit the transaction if no exceptions occur
    except:
        session.rollback()  # Rollback the transaction on exception
        raise
    finally:
        session.close()