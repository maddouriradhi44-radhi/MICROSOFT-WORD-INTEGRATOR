"""
Section Lock model.

This module defines the SectionLock model, which
prevents multiple users from editing the same
section simultaneously.
"""

from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,Integer,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class sectionlock(Base):
    """Represents an active lock on a section
    """

    __tablename__="section_locks"

    # Only one active lock per section
    __table_args__=(
        UniqueConstraint(
        "section_id",
        name="uq_locked_section"
    ),
    )
    # Primary Key
    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrument=True
    )

    # References
    # Locked section
    section_id:Mapped[int]=mapped_column(
        ForeignKey("sections.id"),
        nullable=False
    )

    # User holding the lock
    user_id:Mapped[int]=mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    # Lock Information
    # Lock start time
    locked_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Automatic expiration time
    expires_at:Mapped[datetime]=mapped_column(
        DateTime,
        nullable=False
    )
    
