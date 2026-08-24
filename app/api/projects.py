"""
Project API routes.

This module contains endpoints
related to project management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    UserProjectResponse,
    AddMemberRequest,
    ProjectMemberResponse,
    UpdateMemberRoleRequest,
)

from app.services.project_service import ProjectService
from app.services.project_member_service import ProjectMemberService
from app.services.permission_service import PermissionService

from app.exceptions.project import LastProjectManagerException

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
    response_model=list[UserProjectResponse],
)
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all projects of the authenticated user
    together with their role in each project.
    """

    return ProjectService.get_user_projects(
        db=db,
        user_id=current_user.id,
    )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update project information.

    Only the PROJECT_MANAGER can update the project.
    """

    PermissionService.check_project_manager(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    return ProjectService.update_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        status=data.status,
        ai_enabled=data.ai_enabled,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a project.

    Only the PROJECT_MANAGER can delete the project.
    """

    PermissionService.check_project_manager(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    ProjectService.delete_project(
        db=db,
        project_id=project_id,
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
        user_id=current_user.id,
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
        actor_user_id=current_user.id,
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
    """
    Remove a member from a project.

    Only the PROJECT_MANAGER can remove a member.
    """

    PermissionService.check_project_manager(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    try:
        ProjectMemberService.remove_member(
            db=db,
            project_id=project_id,
            user_id=user_id,
            actor_user_id=current_user.id,
        )
    except LastProjectManagerException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )



@router.patch(
    "/{project_id}/ai",
    response_model=ProjectResponse,
)
def update_project_ai(
    project_id: int,
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    PermissionService.check_project_manager(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    return ProjectService.update_ai_enabled(
        db=db,
        project_id=project_id,
        enabled=enabled,
    )
