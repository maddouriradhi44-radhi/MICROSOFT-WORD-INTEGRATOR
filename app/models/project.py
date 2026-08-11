"""
Project model.

This module defines the Project model,
which represents a collaborative project.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.project_status import ProjectStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project_member import ProjectMember
    from app.models.project_scope import ProjectScope
    from app.models.document import Document


class Project(Base):
    """
    Represents a collaborative project.

    A project contains members, documents,
    and collaboration workflows.
    """

    __tablename__ = "projects"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # ==========================================================
    # Project Information
    # ==========================================================

    # Project name
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Project description
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Current project status
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        default=ProjectStatus.ACTIVE,
        nullable=False
    )

    # ==========================================================
    # Foreign Keys
    # ==========================================================

    # User who created the project
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ==========================================================
    # Audit Information
    # ==========================================================

    # Project creation date
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    # User who owns this project
    owner: Mapped[User] = relationship(
        back_populates="owned_projects"
    )

    # Members participating in this project
    members: Mapped[list[ProjectMember]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    # Documents belonging to this project
    documents: Mapped[list[Document]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    # Project scopes (assigned responsibilities)
    scopes: Mapped[list[ProjectScope]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )
