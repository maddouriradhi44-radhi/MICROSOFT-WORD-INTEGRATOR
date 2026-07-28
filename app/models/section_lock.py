"""
Section Lock model.

This module defines the SectionLock model,
which represents a lock placed on a section
to prevent concurrent editing.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.section import Section
    from app.models.user import User


class SectionLock(Base):
    """
    Represents a lock on a document section.

    A lock prevents multiple users from editing
    the same section simultaneously.
    """

    __tablename__ = "section_locks"

    
    # Primary Key
    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    
    # Foreign Keys
    

    # Locked section
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.id"),
        nullable=False,
        unique=True
    )

    # User holding the lock
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    
    # Lock Information
    

    # Lock creation time
    locked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Lock expiration time
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    
    # Relationships
    

    # Locked section
    section: Mapped[Section] = relationship(
        back_populates="lock"
    )

    # User holding the lock
    user: Mapped[User] = relationship(
        back_populates="section_locks"
    )