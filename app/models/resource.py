#!/usr/bin/env python3
"""Database resources models for DevSaver."""

from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean   
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.engine.db import Base
# from typing import Optional
# from user import User
from datetime import datetime, timezone

class Resource(Base):
    """Model representing a resource in DevSaver."""
    __tablename__ = 'resources'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True, index=True)
    tags: Mapped[str] = mapped_column(String, nullable=True, index=True)
    type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    url: Mapped[str] = mapped_column(String, nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String, nullable=True, index=True)
    source: Mapped[str] = mapped_column(String, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    read_status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    starred: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    
    # Foreign key relationship to User model
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="resources")

    def __repr__(self):
        return f"Resource(id={self.id}, title={self.title}, type={self.type}, source={self.source})"
    
    def to_dict(self) -> dict:
        """Convert Resource instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "type": self.type,
            "url": self.url,
            "original_filename": self.original_filename,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "read_status": self.read_status,
            "starred": self.starred,
            "user_id": self.user_id,
        }