"""
Project Scope model.

This module defines the ProjectScope model,
which represents a responsibility assigned
to a project member.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.project_member import ProjectMember


class ProjectScope(Base):
    """
    Represents a responsibility assigned to a project member.

    A scope defines the functional area
    that a member is responsible for.
    """

    __tablename__ = "project_scopes"

    __table_args__ = (
        UniqueConstraint(
            "project_member_id",
            "name",
            name="uq_project_member_scope"
        ),
    )

    
    # Primary Key
    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    
    # Scope Information
    

    # Scope name
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    # Scope description
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    
    # Foreign Keys
    

    # Related project
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    # Assigned project member
    project_member_id: Mapped[int] = mapped_column(
        ForeignKey("project_members.id"),
        nullable=False
    )

    
    # Audit Information
    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    
    # Relationships
    

    # Project containing this scope
    project: Mapped[Project] = relationship(
        back_populates="scopes"
    )

    # Member responsible for this scope
    project_member: Mapped[ProjectMember] = relationship(
        back_populates="scopes"
    )