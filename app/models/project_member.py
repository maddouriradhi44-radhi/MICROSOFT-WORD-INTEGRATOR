"""
Project Member model.

This module defines the ProjectMember model,
which represents a user's membership in a project.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project
    from app.models.project_scope import ProjectScope

from sqlalchemy import Enum
from app.enums.project_role import ProjectRole

class ProjectMember(Base):
    """
    Represents the association between a user and a project.

    A user can belong to multiple projects,
    and a project can contain multiple users.
    """

    __tablename__ = "project_members"

    # Prevent the same user from being added twice
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_member"
        ),
    )

    
    # Primary Key
    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    
    # Foreign Keys
    # Associated project
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    # Associated user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    
    # Audit Information
    # Date the user joined the project
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    
    # Relationships
    

    # User linked to this membership
    user: Mapped[User] = relationship(
        back_populates="project_memberships"
    )

    # Project linked to this membership
    project: Mapped[Project] = relationship(
        back_populates="members"
    )

    # Responsibilities assigned to this member
    scopes: Mapped[list[ProjectScope]] = relationship(
        back_populates="project_member",
        cascade="all, delete-orphan"
    )

    role: Mapped[ProjectRole] = mapped_column(
    Enum(ProjectRole, name="project_role"),
    nullable=False
    )   