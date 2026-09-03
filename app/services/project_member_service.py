"""
Project member service.

This module contains business logic
related to project team management.
"""

from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember

from app.repositories.project_member_repository import (
    ProjectMemberRepository
)

from app.repositories.project_repository import (
    ProjectRepository
)

from app.repositories.user_repository import (
    UserRepository
)

from app.enums.project_role import ProjectRole

from app.exceptions.project import (
    ProjectNotFoundException,
    LastProjectManagerException,
)

from app.exceptions.user import (
    UserNotFoundException
)

from app.enums.notification_level import NotificationLevel
from app.enums.notification_type import NotificationType

from app.services.notifications_service import NotificationService
from app.services.audit_log_service import AuditLogService
from app.enums.audit_action import AuditAction


class ProjectMemberService:
    """
    Service responsible for project member operations.
    """

    # ==========================================================
    # ADD MEMBER
    # ==========================================================

    @staticmethod
    def add_member(
        db: Session,
        project_id: int,
        email: str,
        role: ProjectRole,
        user_id: int,
    ) -> ProjectMember:
        """
        Add a user to a project.
        """

        # Check project existence
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundException(project_id)

        # Check user existence
        user = UserRepository.get_by_email(
            db,
            email,
        )

        if user is None:
            raise UserNotFoundException(email)

        # Check duplicate membership
        existing_member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user.id,
        )

        if existing_member:
            raise Exception(
                "User is already a member of this project"
            )

        # Create membership
        member = ProjectMember(
            project_id=project_id,
            user_id=user.id,
            role=role,
        )

        member = ProjectMemberRepository.create(
            db,
            member,
        )

        audit_log_service = AuditLogService()

        audit_log_service.log_action(
            db=db,
            user_id=user_id,
            action=AuditAction.CREATE,
            target=f"project_member:{user.id}",
        )

        # Notify the added member
        notification_service = NotificationService()

        notification_service.notify_user(
            db=db,
            user_id=user.id,
            title="Ajout à un projet",
            message=f"Vous avez été ajouté au projet « {project.name} ».",
            notification_type=NotificationType.PROJECT,
            level=NotificationLevel.INFO,
            entity_type="project",
            entity_id=project.id,
        )

        return member

    # ==========================================================
    # GET PROJECT MEMBERS
    # ==========================================================

    @staticmethod
    def get_project_members(
        db: Session,
        project_id: int,
    ) -> list[dict]:
        """
        Return all members of a project
        with their user information.
        """

        project = ProjectRepository.get_by_id(
            db,
            project_id
        )

        if project is None:
            raise ProjectNotFoundException(project_id)

        members = ProjectMemberRepository.get_project_members(
            db,
            project_id
        )

        return [
            {
                "id": member.id,
                "project_id": member.project_id,
                "user_id": member.user_id,
                "role": member.role,
                "joined_at": member.joined_at,
                "first_name": member.user.first_name,
                "last_name": member.user.last_name,
            }
            for member in members
        ]

    # ==========================================================
    # UPDATE MEMBER ROLE
    # ==========================================================

    @staticmethod
    def update_member_role(
        db: Session,
        project_id: int,
        user_id: int,
        new_role: ProjectRole,
        actor_user_id: int,
    ) -> ProjectMember:
        """
        Update member role inside project.
        """

        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user_id,
        )

        if member is None:
            raise UserNotFoundException(user_id)

        # Update the member role
        member = ProjectMemberRepository.update_role(
            db,
            member,
            new_role,
        )

        audit_log_service = AuditLogService()

        audit_log_service.log_action(
            db=db,
            user_id=actor_user_id,
            action=AuditAction.UPDATE,
            target=f"project_member:{user_id}",
        )

        # Get project information
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        # Notify the affected user
        notification_service = NotificationService()

        notification_service.notify_user(
            db=db,
            user_id=user_id,
            title="Rôle du projet modifié",
            message=(
                f"Votre rôle dans le projet "
                f"« {project.name} » a été modifié en "
                f"{new_role.value}."
            ),
            notification_type=NotificationType.PROJECT,
            level=NotificationLevel.INFO,
            entity_type="project",
            entity_id=project_id,
        )

        return member

    # ==========================================================
    # REMOVE MEMBER
    # ==========================================================

    @staticmethod
    def remove_member(
        db: Session,
        project_id: int,
        user_id: int,
        actor_user_id: int,
    ) -> None:
        """
        Remove a member from a project.

        A project must always have at least
        one PROJECT_MANAGER.
        """

        # Get the member
        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user_id,
        )

        if member is None:
            raise UserNotFoundException(user_id)

        # Prevent removing the last project manager
        if member.role == ProjectRole.PROJECT_MANAGER:

            project_manager_count = (
                ProjectMemberRepository.count_project_managers(
                    db,
                    project_id,
                )
            )

            if project_manager_count <= 1:
                raise LastProjectManagerException()

        # Get project information before deleting the member
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundException(project_id)

        # Remove the member
        ProjectMemberRepository.delete(
            db,
            member,
        )

        audit_log_service = AuditLogService()

        audit_log_service.log_action(
            db=db,
            user_id=actor_user_id,
            action=AuditAction.DELETE,
            target=f"project_member:{user_id}",
        )

        # Notify the removed user
        notification_service = NotificationService()

        notification_service.notify_user(
            db=db,
            user_id=user_id,
            title="Removed from Project",
            message=(
                f"You have been removed from the project "
                f"« {project.name} »."
            ),
            notification_type=NotificationType.PROJECT,
            level=NotificationLevel.INFO,
            entity_type="project",
            entity_id=project_id,
        )