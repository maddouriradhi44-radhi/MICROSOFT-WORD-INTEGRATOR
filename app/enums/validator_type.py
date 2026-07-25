"""
Validator type enumeration.
"""

from enum import Enum


class ValidatorType(str, Enum):
    """
    Represents who performed the validation.
    """

    AI = "ai"
    HUMAN = "human"