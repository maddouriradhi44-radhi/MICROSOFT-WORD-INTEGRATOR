"""
Project service.

This module contains business logic
related to project management.
"""

from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_member import ProjectMember

from app.repositories.project_repository import ProjectRepository
from app.repositories.project_member_repository import ProjectMemberRepository
from app.repositories.user_repository import UserRepository

from app.enums.project_role import ProjectRole
from app.enums.notification_level import NotificationLevel
from app.enums.notification_type import NotificationType

from app.exceptions.project import ProjectNotFoundException
from app.exceptions.user import UserNotFoundException

from app.services.notifications_service import NotificationService

from app.enums.project_status import ProjectStatus

class ProjectService:
    """
    Service responsible for project operations.
    """


# ==========================================================
# CREATE PROJECT
# ==========================================================

    @staticmethod
    def create_project(
        db: Session,
        name: str,
        description: str,
        owner_id: int,
    ) -> Project:
        """
        Create a project.

        The creator automatically becomes
        PROJECT_MANAGER.
        """

        user = UserRepository.get_by_id(
            db,
            owner_id,
        )

        if user is None:
            raise UserNotFoundException(owner_id)

        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
        )

        project = ProjectRepository.create(
            db,
            project,
        )

        # Add owner as project manager

        member = ProjectMember(
            project_id=project.id,
            user_id=owner_id,
            role=ProjectRole.PROJECT_MANAGER,
        )

        ProjectMemberRepository.create(
            db,
            member,
        )

        # Notify project owner about project creation

        notification_service = NotificationService()

        notification_service.notify_user(
            db=db,
            user_id=owner_id,
            title="Projet créé",
            message=f"Le projet « {project.name} » a été créé avec succès.",
            notification_type=NotificationType.PROJECT,
            level=NotificationLevel.SUCCESS,
            entity_type="project",
            entity_id=project.id,
        )

        return project

    # ==========================================================
    # GET USER PROJECTS
    # ==========================================================

    @staticmethod
    def get_user_projects(
        db: Session,
        user_id: int,
    ) -> list[dict]:
        """
        Return all projects where the user participates,
        together with the user's role in each project.
        """

        results = ProjectRepository.get_user_projects(
            db,
            user_id,
        )

        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "owner_id": project.owner_id,
                "created_at": project.created_at,
                "role": member.role,
            }
            for project, member in results
        ]

    # ==========================================================
    # UPDATE PROJECT
    # ==========================================================
    @staticmethod
    def update_project(
        db: Session,
        project_id: int,
        name: str | None = None,
        description: str | None = None,
        status: ProjectStatus | None = None,
    ) -> Project:
        """
        Update project information
        and notify all project members.
        """

        # Get the project
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundException(project_id)

        # Get members before updating the project
        members = ProjectMemberRepository.get_project_members(
            db,
            project_id,
        )

        # Update only provided fields
        if name is not None:
            project.name = name

        if description is not None:
            project.description = description

        if status is not None:
            project.status = status

        # Save the project
        project = ProjectRepository.update(
            db,
            project,
        )

        # Notify all project members
        notification_service = NotificationService()

        for member in members:
            notification_service.notify_user(
                db=db,
                user_id=member.user_id,
                title="Projet modifié",
                message=(
                    f"Les informations du projet "
                    f"« {project.name} » ont été modifiées."
                ),
                notification_type=NotificationType.PROJECT,
                level=NotificationLevel.INFO,
                entity_type="project",
                entity_id=project.id,
            )

        return project
    # ==========================================================
    # DELETE PROJECT
    # ==========================================================
    @staticmethod
    def delete_project(
        db: Session,
        project_id: int,
    ) -> None:
        """
        Delete a project and notify all its members.
        """

        # Get the project
        project = ProjectRepository.get_by_id(
            db,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundException(project_id)

        # Save project information before deletion
        project_name = project.name

        # Get members before deleting the project
        members = ProjectMemberRepository.get_project_members(
            db,
            project_id,
        )

        # Notify all project members
        notification_service = NotificationService()

        for member in members:
            notification_service.notify_user(
                db=db,
                user_id=member.user_id,
                title="Projet supprimé",
                message=(
                    f"Le projet « {project_name} » "
                    f"a été supprimé."
                ),
                notification_type=NotificationType.PROJECT,
                level=NotificationLevel.WARNING,
                entity_type="project",
                entity_id=project_id,
            )

        # Delete the project
        ProjectRepository.delete(
            db,
            project,
        )