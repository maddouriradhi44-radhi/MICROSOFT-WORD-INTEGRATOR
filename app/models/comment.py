"""
Comment model.

This module defines the Comment model,
which represents a comment made by a user
on a document section.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text , Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums.comment_status import CommentStatus


from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.section import Section
    from app.enums.comment_status import CommentStatus
    from app.models.comment_mention import CommentMention



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

    # Parent comment
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id"),
        nullable=True,
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

    status: Mapped[CommentStatus] = mapped_column(
    Enum(CommentStatus, name="comment_status"),
    default=CommentStatus.OPEN,
    nullable=False,
    )

     # Parent comment
    parent: Mapped["Comment | None"] = relationship(
        "Comment",
        remote_side=[id],
        back_populates="replies",
    )

    # Replies to this comment
    replies: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    # Users mentioned in this comment
    mentions: Mapped[list["CommentMention"]] = relationship(
        back_populates="comment",
        cascade="all, delete-orphan",
    )