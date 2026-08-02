from enum import Enum


class UserRole(str, Enum):
    PROJECT_MANAGER = "PROJECT_MANAGER"
    COLLABORATOR = "COLLABORATOR"
    READER = "READER"