"""
Notification type enumeration.
"""

from enum import Enum


class NotificationType(str, Enum):
    """
    Represents the category of a notification.
    """

    INFO = "info"
    WARNING = "warning"
    VALIDATION = "validation"
    ASSIGNMENT = "assignment"
    AI_ALERT = "ai_alert"
    SYSTEM = "system"

    