"""
Project API routes.

This module contains endpoints
related to project management.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
     AddMemberRequest,
    ProjectMemberResponse,
    UpdateMemberRoleRequest
)

from app.services.project_service import ProjectService
from app.services.project_member_service import ProjectMemberService
from app.services.permission_service import PermissionService

from app.models.user import User

from app.dependencies.auth_dependency import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new project.

    The authenticated user becomes
    PROJECT_MANAGER automatically.
    """

    project = ProjectService.create_project(
        db=db,
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id,
    )

    return project

@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all projects of the authenticated user.
    """

    return ProjectService.get_user_projects(
        db=db,
        user_id=current_user.id,

    )

@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member(
    project_id: int,
    data: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a user to a project.
    """

    # Check that current user is PROJECT_MANAGER
    PermissionService.check_project_manager(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )


    return ProjectMemberService.add_member(
        db=db,
        project_id=project_id,
        email=data.email,
        role=data.role,
    )

@router.get(
    "/{project_id}/members",
    response_model=list[ProjectMemberResponse],
)
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all members of a project.
    """
    return ProjectMemberService.get_project_members(
    db=db,
    project_id=project_id,
)

@router.put(
    "/{project_id}/members/{user_id}",
    response_model=ProjectMemberResponse,
)
def update_member_role(
    project_id: int,
    user_id: int,
    data: UpdateMemberRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the role of a project member.
    """

    PermissionService.check_project_manager(
    db=db,
    project_id=project_id,
    user_id=current_user.id,
)
    return ProjectMemberService.update_member_role(
    db=db,
    project_id=project_id,
    user_id=user_id,
    new_role=data.role,
)

@router.delete(
    "/{project_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    PermissionService.check_project_manager(
    db=db,
    project_id=project_id,
    user_id=current_user.id,
)
    """
    Remove a member from a project.
    """

    ProjectMemberService.remove_member(
        db=db,
        project_id=project_id,
        user_id=user_id,
    )

    return None