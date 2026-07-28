"""
Comment model.

This module defines the Comment model,
which represents a comment made by a user
on a document section.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.section import Section


class Comment(Base):
    """
    Represents a comment added to a section.

    Comments allow collaborators to discuss
    changes or provide feedback.
    """

    __tablename__ = "comments"

    
    # Primary Key
    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    
    # Comment Information
    

    # Comment content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    
    # Foreign Keys
    

    # Related section
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.id"),
        nullable=False
    )

    # Comment author
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    
    # Audit Information
    

    # Date and time when the comment was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    
    # Relationships
    

    # Section containing this comment
    section: Mapped[Section] = relationship(
        back_populates="comments"
    )

    # User who wrote the comment
    author: Mapped[User] = relationship(
        back_populates="comments"
    )