"""
Project member repository.

This module contains all database operations
related to the ProjectMember model.

By centralizing database queries in one place,
the code becomes easier to maintain, test,
and extend over time.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember
from app.enums.project_role import ProjectRole


class ProjectMemberRepository:
    """
    Repository responsible for ProjectMember
    database operations.
    """

    @staticmethod
    def create(
        db: Session,
        member: ProjectMember,
    ) -> ProjectMember:
        """
        Save a new project member to the database.

        Args:
            db: Active database session.
            member: ProjectMember instance to save.

        Returns:
            The saved ProjectMember instance.
        """

        db.add(member)
        db.commit()
        db.refresh(member)

        return member

    @staticmethod
    def update(
        db: Session,
        member: ProjectMember,
    ) -> ProjectMember:
        """
        Update an existing project member.
        """

        db.commit()
        db.refresh(member)

        return member


    @staticmethod
    def get_project_members(
        db: Session,
        project_id: int,
    ) -> list[ProjectMember]:
        """
        Return all members of a project.
        """

        result = db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id
            )
        )

        return list(result.scalars().all())

    @staticmethod
    def update_role(
        db: Session,
        member: ProjectMember,
        new_role:ProjectRole
    ) -> ProjectMember:
        """
        Update the role of a project member.

        Returns:
            The updated ProjectMember instance.
        """

        member.role = new_role

        db.commit()
        db.refresh(member)

        return member

    @staticmethod
    def delete(
        db: Session,
        member: ProjectMember,
    ) -> None:
        """
        Remove a member from a project.
        """

        db.delete(member)
        db.commit()

    @staticmethod
    def get_by_project_and_user(
        db: Session,
        project_id: int,
        user_id: int,
    ) -> ProjectMember | None:
        """
        Return a project membership if the user
        already belongs to the project.
        """

        result = db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()


    @staticmethod
    def count_project_managers(
        db: Session,
        project_id: int,
    ) -> int:
        """
        Count the number of project managers
        in a project.
        """

        result = db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.role == ProjectRole.PROJECT_MANAGER,
            )
        )

        return len(result.scalars().all())