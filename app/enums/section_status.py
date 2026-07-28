"""Section status enum.

This module defines the possible states of a document section
throughout its editing and validation lifecycle.
"""

import enum


class SectionStatus(str, enum.Enum):
    """Possible states of a section."""

    IN_PROGRESS = "in_progress"
    PENDING_VALIDATION = "pending_validation"
    VALIDATED = "validated"
    REJECTED = "rejected"