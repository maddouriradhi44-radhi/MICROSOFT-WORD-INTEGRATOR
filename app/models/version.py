"""
Version model.

This module defines the Version model,
which represents a version of a document section.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text, String, Boolean , Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums.version_change import VersionChangeType

from app.database.base import Base

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

    # Snapshot of the section title at this version
    title_snapshot: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    # Snapshot of the section content at this version
    content_snapshot: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    # Explanation of changes made in this version
    change_comment: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # Indicates if this is the current active version
    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    change_type: Mapped[VersionChangeType] = mapped_column(
        Enum(
            VersionChangeType,
            name="version_change_type"
        ),
        default=VersionChangeType.UPDATE,
        nullable=False
    )

    # Indicates if this version is archived
    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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

    # Previous version reference
    parent_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("versions.id"),
        nullable=True
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

    # Previous version
    parent_version: Mapped["Version | None"] = relationship(
        remote_side="Version.id",
        back_populates="child_versions",
        uselist=False
    )


    # Versions created from this version
    child_versions: Mapped[list["Version"]] = relationship(
        back_populates="parent_version"
    )