"""
Permission service.

This module contains business logic
related to authorization and permissions.
"""

from sqlalchemy.orm import Session

from app.enums.project_role import ProjectRole

from app.exceptions.permission import PermissionDeniedException

from app.models.project_member import ProjectMember
from app.models.section import Section

from app.repositories.project_member_repository import (
    ProjectMemberRepository,
)


class PermissionService:
    """
    Service responsible for permission checks.
    """

    @staticmethod
    def get_project_member(
        db: Session,
        project_id: int,
        user_id: int,
    ) -> ProjectMember:
        """
        Retrieve a user's membership in a project.
        """

        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user_id,
        )

        if member is None:
            raise PermissionDeniedException()

        return member


    @staticmethod
    def get_project_role(
        db: Session,
        project_id: int,
        user_id: int,
    ) -> ProjectRole:
        """
        Retrieve a user's role in a project.
        """

        member = PermissionService.get_project_member(
            db,
            project_id,
            user_id,
        )

        return member.role

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

        member = PermissionService.get_project_member(
            db,
            project_id,
            user_id,
        )

        PermissionService.require_project_manager(
            member,
        )

    @staticmethod
    def check_section_editor(
        db: Session,
        section: Section,
        user_id: int,
    ) -> bool:
        """
        Check if a user can edit a section.

        Rules:
        - PROJECT_MANAGER -> all sections.
        - COLLABORATOR -> only assigned sections.
        """

        member = PermissionService.get_project_member(
            db,
            section.project_id,
            user_id,
        )

        # Project manager
        if member.role == ProjectRole.PROJECT_MANAGER:
            return True

        # Assigned collaborator
        if (
            member.role == ProjectRole.COLLABORATOR
            and section.assigned_user_id == user_id
        ):
            return True

        raise PermissionDeniedException()


    