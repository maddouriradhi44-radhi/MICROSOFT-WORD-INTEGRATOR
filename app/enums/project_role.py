from enum import Enum


class ProjectRole(str, Enum):
    PROJECT_MANAGER = "PROJECT_MANAGER"
    COLLABORATOR = "COLLABORATOR"
    READER = "READER"