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

from app.exceptions.project import ProjectNotFoundException
from app.exceptions.user import UserNotFoundException



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
            owner_id
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
            project
        )



        # Add owner as project manager

        member = ProjectMember(
            project_id=project.id,
            user_id=owner_id,
            role=ProjectRole.PROJECT_MANAGER,
        )


        ProjectMemberRepository.create(
            db,
            member
        )


        return project




    # ==========================================================
    # GET USER PROJECTS
    # ==========================================================

    @staticmethod
    def get_user_projects(
        db: Session,
        user_id: int,
    ) -> list[Project]:
        """
        Return all projects where user participates.
        """


        return ProjectRepository.get_user_projects(
            db,
            user_id
        )




    # ==========================================================
    # UPDATE PROJECT
    # ==========================================================

    @staticmethod
    def update_project(
        db: Session,
        project_id: int,
        name: str,
        description: str,
    ) -> Project:
        """
        Update project information.
        """


        project = ProjectRepository.get_by_id(
            db,
            project_id
        )


        if project is None:
            raise ProjectNotFoundException(project_id)



        project.name = name
        project.description = description



        return ProjectRepository.update(
            db,
            project
        )




    # ==========================================================
    # DELETE PROJECT
    # ==========================================================

    @staticmethod
    def delete_project(
        db: Session,
        project_id: int,
    ) -> None:
        """
        Delete a project.
        """


        project = ProjectRepository.get_by_id(
            db,
            project_id
        )


        if project is None:
            raise ProjectNotFoundException(project_id)



        ProjectRepository.delete(
            db,
            project
        )