"""
Audit Log model.

This module defines the AuditLog model,
which records important actions performed
within the application.
"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.audit_action import AuditAction

class AuditLog(Base):
    """
    Represents an audit record.
    """

    # Database table name
    __tablename__ = "audit_logs"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # References
    # User who performed the action
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Audit Information
    # Action performed
    action: Mapped[AuditAction] = mapped_column(
        Enum(AuditAction, name="audit_action"),
        nullable=False
    )

    # Type of resource affected
    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Identifier of the affected resource
    resource_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Additional details about the action
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    # Audit Date
    # Date and time of the action
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
