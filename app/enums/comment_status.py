from enum import Enum


class CommentStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"