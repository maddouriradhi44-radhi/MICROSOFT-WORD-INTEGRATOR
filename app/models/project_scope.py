"""
Project Scope model.

This module defines the ProjectScope model, which
assigns project modules to project members.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint

from app.database.base import Base


class ProjectScope(Base):
    """
    Represents a responsibility assigned to a project member.

    Each record indicates that a project member is responsible
    for a specific module within the project.
    """

    # Database table name
    __tablename__ = "project_scopes"

     # Prevent assigning the same module twice to the same project member
    __table_args__ = (
        UniqueConstraint(
            "project_member_id",
            "module_id",
            name="uq_project_member_module"
        ),
    )

      
    # Primary Key
    # Unique identifier
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

      
    # References
    # Project member assigned to the module
    project_member_id: Mapped[int] = mapped_column(
        ForeignKey("project_members.id"),
        nullable=False
    )

    # Assigned module
    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id"),
        nullable=False
    )

    # Audit Information
    # Assignment creation date
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    