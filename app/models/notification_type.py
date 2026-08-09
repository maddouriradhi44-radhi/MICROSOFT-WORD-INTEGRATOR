from enum import Enum


class NotificationType(str, Enum):
    ASSIGNMENT = "ASSIGNMENT"
    VALIDATION = "VALIDATION"
    REJECTION = "REJECTION"
    MODIFICATION = "MODIFICATION"
    MENTION = "MENTION"
    SYSTEM = "SYSTEM"