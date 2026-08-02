"""
Project repository.

This module contains all database operations
related to the Project model.

By centralizing database queries in one place,
the code becomes easier to maintain, test,
and extend over time.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_member import ProjectMember


class ProjectRepository:
    """Repository responsible for Project database operations."""

    @staticmethod
    def create(
     db: Session,
    project: Project,
    ) -> Project:
        """
        Save a new project to the database.

        Args:
            db: Active database session.
            project: Project instance to save.

        Returns:
            The saved Project instance.
        """

        db.add(project)
        db.commit()
        db.refresh(project)

        return project

    @staticmethod
    def get_by_id(
        db: Session,
        project_id: int,
    ) -> Project | None:
        """
        Return a project by its id.

        Returns None if no project exists.
        """

        result = db.execute(
            select(Project).where(Project.id == project_id)
        )

        return result.scalar_one_or_none()


    @staticmethod
    def get_user_projects(
        db: Session,
        user_id: int,
    ) -> list[Project]:
        """
        Return all projects where the user is a member.
        """

        result = db.execute(
            select(Project)
            .join(ProjectMember)
            .where(ProjectMember.user_id == user_id)
        )

        return list(result.scalars().all())

    
    @staticmethod
    def update(
        db: Session,
        project: Project,
    ) -> Project:
        """
        Update an existing project.

        Returns:
            The updated Project instance.
        """

        db.commit()
        db.refresh(project)

        return project


    @staticmethod
    def delete(
        db: Session,
        project: Project,
    ) -> None:
        """
        Delete an existing project.
        """

        db.delete(project)
        db.commit()

    @staticmethod
    def get_owned_projects(
        db: Session,
        owner_id: int,
    ) -> list[Project]:
        """
        Return projects created by a user.
        """

        result = db.execute(
            select(Project)
            .where(Project.owner_id == owner_id)
        )

        return list(result.scalars().all())