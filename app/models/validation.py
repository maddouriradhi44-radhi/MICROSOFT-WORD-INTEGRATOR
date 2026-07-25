"""
Validation model.

This module defines the Validation model,
which stores the result of validating
a proposed version.
"""
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.validation_status import ValidationStatus
from app.enums.validator_type import ValidatorType

class Validation(Base):
    """
    Represents the validation result
    of a version.
    """

    # Database table name
    __tablename__ = "validations"

    # Primary Key
    d: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # References
    # Version being validated
    version_id: Mapped[int] = mapped_column(
        ForeignKey("versions.id"),
        nullable=False,
        unique=True
    )

    # Human reviewer (NULL if AI validates)
    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # Validation Information
    #Validator type (AI or Human)
    validator_type: Mapped[ValidatorType] = mapped_column(
        Enum(ValidatorType, name="validator_type"),
        nullable=False
    )

    # AI confidence score (0 - 100)
    ai_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    # Validation result
    status: Mapped[ValidationStatus] = mapped_column(
        Enum(ValidationStatus, name="validation_status"),
        default=ValidationStatus.PENDING,
        nullable=False
    )

    # Audit Information
    # Validation date
    validated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    