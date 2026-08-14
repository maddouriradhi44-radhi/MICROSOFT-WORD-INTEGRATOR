"""
Validation schemas.

This module contains Pydantic schemas
used by the validation API.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.validation_status import ValidationStatus


class ValidationCreate(BaseModel):
    """
    Schema used to create a validation.
    """

    version_id: int


class ValidationDecision(BaseModel):
    """
    Schema used by the project manager
    to approve or reject a validation.
    """

    comment: str | None = None


class ValidationResponse(BaseModel):
    """
    Schema returned by the validation API.
    """

    id: int
    status: ValidationStatus
    comment: str | None
    validated_by_ai: bool
    version_id: int
    reviewer_id: int | None
    validated_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )

    