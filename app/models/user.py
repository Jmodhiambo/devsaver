#!/usr/bin/env python3
"""Database user model for DevSaver."""

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.engine.db import Base
from app.models.resource import Resource
from typing import List, Optional
from datetime import datetime, timezone

class User(Base):
    """Model representing a user in DevSaver."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    fullname: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255, collation="NOCASE"), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_login_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    resources: Mapped[List[Resource]] = relationship("Resource", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
    def to_dict(self, include_password:bool = False) -> dict:
        """Convert User instance to dictionary."""
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }
        if include_password:
            data["password_hash"] = self.password_hash
        return data