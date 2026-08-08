"""
Comment mention model.

This module defines the CommentMention model,
which represents a user mentioned in a comment.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.user import User


class CommentMention(Base):
    """
    Represents a user mentioned in a comment.
    """

    __tablename__ = "comment_mentions"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Comment containing the mention
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id"),
        nullable=False,
    )

    # Mentioned user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # Relationships

    comment: Mapped["Comment"] = relationship(
        back_populates="mentions",
    )

    user: Mapped["User"] = relationship(
        back_populates="comment_mentions",
    )

