"""
Document model.

This module defines the Document model, which represents
a Word document managed by the application.
"""

from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.base import Base
from app.enums.document_status import DocumentStatus


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import project
    from app.models.section import Section


class Document(Base):
    """
    Represents a collaborative Word document.

    A document is imported by a user and contains
    one or more editable sections.
    """

    __tablename__ = "documents"

    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    #Document title
    title:Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    # Absolute or relative path of the .docx file
    file_path: Mapped[str] = mapped_column(
    String(500),
    nullable=False
    )

    status: Mapped[DocumentStatus] = mapped_column(
    Enum(DocumentStatus, name="document_status"),
    default=DocumentStatus.IN_PROGRESS,
    nullable=False
)

     # User who imported the document
    owner_id:Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    #Date and time when the document was imported
    imported_at: Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
 # User who imported this document
    owner: Mapped[User] = relationship(
        back_populates="documents"
    )

    # Project containing this document
    project: Mapped[project] = relationship(
        back_populates="documents"
    )

    # Sections contained in this document
    sections: Mapped[list[Section]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan"
    )    

