"""
Comment model.

This module defines the comment model,which stores
 comments made on document sections
"""

from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,Integer,Text
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class comment(Base):
    """
    Represents a comment left on a section 
    """

    __tablename__="comments"

    #Primary key
    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # References
     # Section concerned by the comment
    section_id: Mapped[int] = mapped_column(
        ForeignKey("section.id"),
        nullable=False
    )

    # User who wrote the comment
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Comment Information
    # Comment content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Creation date
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Version on which the comment was made
    version_id: Mapped[int] = mapped_column(
    ForeignKey("versions.id"),
    nullable=False
)

