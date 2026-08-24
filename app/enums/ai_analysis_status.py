"""
AI analysis status enumeration.
"""

from enum import Enum


class AIAnalysisStatus(str, Enum):
    """
    Represents the lifecycle of an AI analysis.
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"