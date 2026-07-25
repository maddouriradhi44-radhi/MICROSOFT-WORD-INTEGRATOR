"""
Section model.

This module defines the Section model, which represents
an editable section of a collaborative Word document.
"""

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.section_status import SectionStatus


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

    