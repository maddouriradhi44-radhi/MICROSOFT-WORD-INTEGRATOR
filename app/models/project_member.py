"""
Project Member model.

This module defines the ProjectMember model,
which links users to collaborative projects.
"""

from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Integer
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class projectMember(Base):
    """
    Represents a membership between a user and a project 
    """

    #Database table name
    __tablename__="project_members"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

     # References
    # Project identifier
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
       )

      # Audit Information
      # Date and time when the user joined the project
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )