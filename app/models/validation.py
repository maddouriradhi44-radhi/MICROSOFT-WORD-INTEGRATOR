"""
Validation model.

This module defines the Validation model,
which represents the validation of a document version.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.validation_status import ValidationStatus

if TYPE_CHECKING:
    from app.models.version import Version
    from app.models.user import User
    from app.models.ai_validation_report import AIValidationReport


class Validation(Base):
    """
    Represents the validation of a version.

    A validation can be performed automatically
    by the AI or manually by the project manager.
    """

    __tablename__ = "validations"

    
    # Primary Key
    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    
    # Validation Information
    

    # Validation status
    status: Mapped[ValidationStatus] = mapped_column(
        Enum(
            ValidationStatus,
            name="validation_status"
        ),
        default=ValidationStatus.PENDING,
        nullable=False
    )

    # Reviewer's comment
    comment: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # Indicates whether the validation
    # was performed automatically by the AI
    validated_by_ai: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    
    # Foreign Keys
    

    # Version being validated
    version_id: Mapped[int] = mapped_column(
        ForeignKey("versions.id"),
        nullable=False,
        unique=True
    )

    # Project manager who reviewed the version
    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    
    # Audit Information
    

    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    
    # Relationships
    

    # Version associated with this validation
    version: Mapped[Version] = relationship(
        back_populates="validation"
    )

    # User who reviewed this validation
    reviewer: Mapped[User | None] = relationship(
        back_populates="validations"
    )

    ai_report: Mapped[AIValidationReport | None] = relationship(
        back_populates="validation",
        uselist=False,
        cascade="all, delete-orphan",
    )