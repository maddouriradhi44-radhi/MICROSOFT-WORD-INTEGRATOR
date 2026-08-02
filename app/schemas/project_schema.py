"""
Project Pydantic schemas.

This module defines the request and response schemas
used by the Project Management API.
"""

from pydantic import BaseModel, ConfigDict

from app.enums.project_status import ProjectStatus
from app.enums.project_role import ProjectRole
from datetime import datetime
from pydantic import Field, EmailStr

class ProjectCreate(BaseModel):
    """
    Schema used when creating a project.

    The creator automatically becomes
    PROJECT_MANAGER.
    """

    name: str = Field(
        min_length=3,
        max_length=255
    )

    description: str = Field(
        min_length=10
    )


class ProjectUpdate(BaseModel):
    """
    Schema used to update an existing project.
    """

    name: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectResponse(BaseModel):
    """
    Schema returned to the client.
    """

    id: int
    name: str
    description: str
    status: ProjectStatus
    owner_id: int
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)


class AddMemberRequest(BaseModel):
    """
    Schema used to add a member to a project.
    """

    email: EmailStr
    role: ProjectRole


class UpdateMemberRoleRequest(BaseModel):
    """
    Schema used to update a member's role.
    """

    role: ProjectRole   


class ProjectMemberResponse(BaseModel):
    """
    Schema returned for project members.
    """

    id: int
    project_id: int
    user_id: int
    role: ProjectRole
    joined_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

    