from enum import Enum


class NotificationType(str, Enum):
    SECURITY = "SECURITY"
    PROJECT = "PROJECT"
    DOCUMENT = "DOCUMENT"
    SECTION = "SECTION"
    COMMENT = "COMMENT"
    MENTION = "MENTION"
    VALIDATION = "VALIDATION"
    VERSION = "VERSION"
    LOCK = "LOCK"
    SCHEDULER = "SCHEDULER"
    AI = "AI"