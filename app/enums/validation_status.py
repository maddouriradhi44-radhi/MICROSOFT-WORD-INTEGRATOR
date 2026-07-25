"""
Validation status enumeration.
"""

from enum import Enum


class ValidationStatus(str, Enum):
    """
    Represents the result of a validation.
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"