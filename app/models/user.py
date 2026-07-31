from __future__ import annotations

"""User model.

This module defines the User model, which represents
an application user in the database.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.user_role import UserRole

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog
    from app.models.comment import Comment
    from app.models.document import Document
    from app.models.notification import Notification
    from app.models.project import Project
    from app.models.project_member import ProjectMember
    from app.models.section_lock import SectionLock

    from app.models.audit_log import AuditLog
from datetime import datetime
from sqlalchemy import DateTime,Enum,Integer,String,Boolean
from sqlalchemy.orm import Mapped , mapped_column,relationship 

    from app.models.validation import Validation
    from app.models.version import Version



class User(Base):
    """
    Represents an application user.

    A user can:
    - Sign in to the application.
    - Import documents.
    - Edit assigned sections.
    - Collaborate with other users.
    """

    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Personal Information
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Authentication
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Email verification
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    verification_token: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    verification_token_expires: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Password reset
    reset_token: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    reset_token_expires: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_roles"),
        nullable=False,
    )

    # Audit information
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships

    # Projects created by this user
    owned_projects: Mapped[list["Project"]] = relationship(
        back_populates="owner"
    )

    # Projects where the user is a member
    project_memberships: Mapped[list["ProjectMember"]] = relationship(
        back_populates="user"
    )

    # Documents imported by this user
    documents: Mapped[list["Document"]] = relationship(
        back_populates="owner"
    )

    # Versions created by this user
    versions: Mapped[list["Version"]] = relationship(
        back_populates="author"
    )

    # Comments written by this user
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author"
    )

    # Validations performed by this user
    validations: Mapped[list["Validation"]] = relationship(
        back_populates="reviewer"
    )

    # Notifications received by this user
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Sections currently locked by this user
    section_locks: Mapped[list["SectionLock"]] = relationship(
        back_populates="user"
    )

    # Audit log entries created by this user
     audit_logs: Mapped[list[AuditLog]] = relationship(
        back_populates="user" ,
        cascade="all, delete-orphan"
    )

     # Email verification
     is_verified: Mapped[bool] = mapped_column(
         Boolean,
         default=False,
        nullable=False
    )

     verification_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

     verification_token_expires: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

# Password reset
     reset_token: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True
    )

     reset_token_expires: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    ) 

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

