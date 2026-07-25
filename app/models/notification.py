"""
Notification model.

This module defines the Notification model,
which stores notifications sent to users.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.notification_type import NotificationType


class Notification(Base):
    """
    Represents a notification sent to a user.
    """

    # Database table name
    __tablename__ = "notifications"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # References
    # Recipient of the notification
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Notification Information
    # Notification title
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Notification message
    message: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    # Notification category
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type"),
        nullable=False
    )

    # Indicates whether the notification has been read
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Audit Information
    # Notification creation date
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
