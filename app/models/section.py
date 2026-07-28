"""
Section model.

This module defines the Section model, which represents
an editable section of a collaborative Word document.
"""

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.base import Base
from app.enums.section_status import SectionStatus

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.version import Version
    from app.models.comment import Comment
    from app.models.section_lock import SectionLock


class Section(Base):
    """
    Represents a section inside a document.

    Each section can be assigned to collaborators,
    locked during editing, versioned, and validated.
    """

     # Database table name
    __tablename__ = "sections"

     
    # Primary Key
    # Unique identifier for each section
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    # Document Reference
    # Document that owns this section
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False
    )

    project_id: Mapped[int] = mapped_column(
    ForeignKey("projects.id"),
    nullable=False
    )

    # Section Information
    # Section title extracted from the Word document
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    # Section content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Heading level (Heading 1, Heading 2, ...)
    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Position inside the document
    order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    # Workflow
    # Current section status
    status: Mapped[SectionStatus] = mapped_column(
        Enum(SectionStatus, name="section_status"),
        default=SectionStatus.IN_PROGRESS,
        nullable=False
    )

    # Indicates whether the section is currently locked
    is_locked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Module to which this section belongs
    module: Mapped[str] = mapped_column(
    String(100),
    nullable=False
)

 # Relationships
  # Parent document
    document: Mapped[Document] = relationship(
        back_populates="sections"
    )

    # All versions of this section
    versions: Mapped[list[Version]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )

    # Comments on this section
    comments: Mapped[list[Comment]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )

    # Current lock for this section
    lock: Mapped[SectionLock | None] = relationship(
        back_populates="section",
        uselist=False,
        cascade="all, delete-orphan"
    )
    