"""User model

This module defines the User model,witch represents 
an application user in the database.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.project_member import ProjectMember
    from app.models.document import Document
    from app.models.version import Version
    from app.models.comment import Comment
    from app.models.validation import Validation
    from app.models.notification import Notification
    from app.models.section_lock import SectionLock
    from app.models.audit_log import AuditLog
from datetime import datetime
from sqlalchemy import DATETIME,Enum,Integer,String
from sqlalchemy import Mapped , mapped_column,relationship 

from app.database.base import Base
from app.enums.user_role import UserRole

class User(Base):
     """
    Represents an application user.

    A user can:
    - Sign in to the application.
    - Import documents.
    - Edit assigned sections.
    - Collaborate with other users.
    """
     __tablename__="users"

     id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Personal Information 
     first_name: Mapped[str] = mapped_column(
         String(100),
         nullable=False
        
    )

     last_name: Mapped[str] = mapped_column(
          String(100),
          nullable=False
     )

    # Authentication 
     email:Mapped[str]=mapped_column(
          String(150),
          unique=True,
          nullable=False
     )    

    #User's hashed passworf(bcrypt)
     password_hush:Mapped[str]= mapped_column(
          String(255),
          nullable=False  
    ) 

     role:Mapped[UserRole]=mapped_column(
          Enum(UserRole,name="user_roles"),
          nullable=False
     )

     # Audit Information 
     #Date and time when the account was created 

     created_at: Mapped[datetime]=mapped_column(
          DATETIME,
          default=datetime.utcnow,
          nullable=False
     )

     # Projects created by this user
     owned_projects: Mapped[list[Project]] = relationship(
        back_populates="owner"
    )

    # Projects where the user is a member
     project_memberships: Mapped[list[ProjectMember]] = relationship(
        back_populates="user"
    )

    # Documents imported by this user
     documents: Mapped[list[Document]] = relationship(
        back_populates="owner"
    )

    # Versions created by this user
     versions: Mapped[list[Version]] = relationship(
        back_populates="author"
    )

    # Comments written by this user
     comments: Mapped[list[Comment]] = relationship(
        back_populates="author"
    )

    # Validations performed by this user
     validations: Mapped[list[Validation]] = relationship(
        back_populates="reviewer"
    )

    # Notifications received by this user
     notifications: Mapped[list[Notification]] = relationship(
        back_populates="user",
        cascade="qll, deletre-orphan"
    )

    # Sections currently locked by this user
     section_locks: Mapped[list[SectionLock]] = relationship(
        back_populates="user"
    )

    # Audit log entries created by this user
     audit_logs: Mapped[list[AuditLog]] = relationship(
        back_populates="user" ,
        cascade="all , delete-orphan"
    )