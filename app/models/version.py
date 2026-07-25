"""
Version model.

This module defines the Version model, which stores
the content history and validation status of a section
over time.
"""

from datetime import datetime
from sqlalchemy import DateTime,Enum,ForeignKey,Integer,Text
from sqlalchemy.orm import mapped_column,Mapped

from app.database.base import Base

class version(Base):
    """
    Represents a saved version of a section.
    """
    __tablename__="versions"

    #primary Key
    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=False
    )

    # References
    # Section concerned by this version
    user_id:Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    #Version information 
    version_number:Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Section content at this version
    content:Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

      # Creation date
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
