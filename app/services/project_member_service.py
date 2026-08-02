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
    ProjectNotFoundException
)

from app.exceptions.user import (
    UserNotFoundException
)


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
    ) -> ProjectMember:
        """
        Add a user to a project.
        """


        # Check project existence
        project = ProjectRepository.get_by_id(
            db,
            project_id
        )

        if project is None:
            raise ProjectNotFoundException(project_id)



        # Check user existence
        user = UserRepository.get_by_email(
            db,
            email
        )

        print("SEARCH EMAIL =", email)
        print("FOUND USER =", user)

        if user is None:
            raise UserNotFoundException(email)



        # Check duplicate membership
        existing_member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user.id
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


        return ProjectMemberRepository.create(
            db,
            member
        )



    # ==========================================================
    # GET PROJECT MEMBERS
    # ==========================================================

    @staticmethod
    def get_project_members(
        db: Session,
        project_id: int,
    ) -> list[ProjectMember]:
        """
        Return all members of a project.
        """


        project = ProjectRepository.get_by_id(
            db,
            project_id
        )


        if project is None:
            raise ProjectNotFoundException(project_id)



        return ProjectMemberRepository.get_project_members(
            db,
            project_id
        )



    # ==========================================================
    # UPDATE MEMBER ROLE
    # ==========================================================

    @staticmethod
    def update_member_role(
        db: Session,
        project_id: int,
        user_id: int,
        new_role: ProjectRole,
    ) -> ProjectMember:
        """
        Update member role inside project.
        """


        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user_id
        )


        if member is None:
            raise UserNotFoundException(user_id)



        return ProjectMemberRepository.update_role(
            db,
            member,
            new_role
        )



    # ==========================================================
    # REMOVE MEMBER
    # ==========================================================

    @staticmethod
    def remove_member(
        db: Session,
        project_id: int,
        user_id: int,
    ) -> None:
        """
        Remove a member from a project.
        """


        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            project_id,
            user_id
        )


        if member is None:
            raise UserNotFoundException(user_id)



        ProjectMemberRepository.delete(
            db,
            member
        )