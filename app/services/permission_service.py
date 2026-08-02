"""
Permission service.

This module contains business logic
related to authorization and permissions.
"""

from sqlalchemy.orm import Session

from app.enums.project_role import ProjectRole
from app.exceptions.permission import PermissionDeniedException

from app.models.project_member import ProjectMember

from app.repositories.project_member_repository import (
    ProjectMemberRepository
)


class PermissionService:
    """
    Service responsible for permission checks.
    """


    @staticmethod
    def require_project_manager(
        member: ProjectMember,
    ) -> None:
        """
        Ensure that the member is a project manager.
        """

        if member.role != ProjectRole.PROJECT_MANAGER:
            raise PermissionDeniedException()



    @staticmethod
    def check_project_manager(
        db: Session,
        project_id: int,
        user_id: int,
    ) -> None:
        """
        Check if a user is project manager of a project.
        """


        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user_id,
        )


        if member is None:
            raise PermissionDeniedException()


        PermissionService.require_project_manager(
            member
        )