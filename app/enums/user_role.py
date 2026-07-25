from enum import Enum

class UserRole(str, Enum):
    PROJECT_MANAGER = "project_manager"
    COLLABORATOR = "collaborator"
    VIEWER = "viewer"
