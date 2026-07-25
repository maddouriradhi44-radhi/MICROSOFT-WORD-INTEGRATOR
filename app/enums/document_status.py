"""
Document status enumeration.
"""
from enum import Enum

class DocumentStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    FINALIZED = "finalized"