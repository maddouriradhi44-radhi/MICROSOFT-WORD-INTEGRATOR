"""
Audit Log model.

This module defines the AuditLog model,
which stores every important action
performed in the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(Base):
    """
    Represents an audit log entry.
    """

    __tablename__ = "audit_logs"

    
    # Primary Key
    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    
    # Audit Information
    

    action: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    target: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    
    # Foreign Keys
    

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    
    # Timestamp
    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    
    # Relationships
    

    user: Mapped[User] = relationship(
        back_populates="audit_logs"
    )