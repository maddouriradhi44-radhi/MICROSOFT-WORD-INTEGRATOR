"""
Version model.

This module defines the Version model,
which represents a version of a document section.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.validation_status import ValidationStatus

if TYPE_CHECKING:
    from app.models.section import Section
    from app.models.user import User
    from app.models.validation import Validation


class Version(Base):
    """
    Represents a version of a section.

    Each modification creates a new version
    that can be validated before becoming official.
    """

    __tablename__ = "versions"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # ==========================================================
    # Version Information
    # ==========================================================

    # Sequential version number
    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Section content for this version
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Validation status
    validation_status: Mapped[ValidationStatus] = mapped_column(
        Enum(
            ValidationStatus,
            name="validation_status"
        ),
        default=ValidationStatus.PENDING,
        nullable=False
    )

    # ==========================================================
    # Foreign Keys
    # ==========================================================

    # Related section
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.id"),
        nullable=False
    )

    # User who created this version
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ==========================================================
    # Audit Information
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    # Parent section
    section: Mapped[Section] = relationship(
        back_populates="versions"
    )

    # User who created this version
    author: Mapped[User] = relationship(
        back_populates="versions"
    )

    # Validation associated with this version
    validation: Mapped[Validation | None] = relationship(
        back_populates="version",
        uselist=False,
        cascade="all, delete-orphan"
    )