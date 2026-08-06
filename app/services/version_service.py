"""
Version service.

This module contains business logic
related to document section versions.
"""

from sqlalchemy.orm import Session

from app.models.version import Version

from app.repositories.version_repository import (
    VersionRepository,
)
from app.enums.version_change import VersionChangeType

class VersionService:
    """
    Service responsible for version management.
    """


    def __init__(self):
        self.repository = VersionRepository()



    def create_new_version(
        self,
        db: Session,
        section_id: int,
        author_id: int,
        title_snapshot: str,
        content_snapshot: str,
        change_comment: str | None = None,
        change_type: VersionChangeType = VersionChangeType.UPDATE,
    ) -> Version:
        """
        Create a new version for a section.
        """

        latest_number = (
            self.repository.get_latest_version_number(
                db,
                section_id,
            )
        )


        current_version = (
            self.repository.get_current_version(
                db,
                section_id,
            )
        )


        if current_version:
            current_version.is_current = False


        version = Version(
            section_id=section_id,
            author_id=author_id,
            version_number=latest_number + 1,
            title_snapshot=title_snapshot,
            content_snapshot=content_snapshot,
            change_comment=change_comment,
            change_type=change_type,
            is_current=True,
        )

        if current_version:
            version.parent_version_id = current_version.id


        return self.repository.create_version(
            db,
            version,
        )


    def get_history(
        self,
        db: Session,
        section_id: int,
    ) -> list[Version]:
        """
        Retrieve all versions of a section.
        """

        return self.repository.get_section_versions(
            db,
            section_id,
        )



    def get_current_version(
        self,
        db: Session,
        section_id: int,
    ) -> Version | None:
        """
        Retrieve the current active version.
        """

        return self.repository.get_current_version(
            db,
            section_id,
        )



    def restore_version(
        self,
        db: Session,
        version_id: int,
        author_id: int,
    ) -> Version | None:
        """
        Restore a previous version.

        A restore operation creates
        a new version instead of deleting history.
        """

        old_version = (
            self.repository.get_version_by_id(
                db,
                version_id,
            )
        )


        if old_version is None:
            return None


        return self.create_new_version(
            db,
            section_id=old_version.section_id,
            author_id=author_id,
            title_snapshot=old_version.title_snapshot,
            content_snapshot=old_version.content_snapshot,
            change_comment=f"Restore version {old_version.version_number}",
            change_type=VersionChangeType.RESTORE,
        )


    def archive_version(
        self,
        db: Session,
        version_id: int,
        user_id: int,
    ):
        version = (
            self.repository.get_version_by_id(
                db,
                version_id,
            )
        )

        if version is None:
            return None

        version.is_archived = True
        version.is_current = False

        db.commit()
        db.refresh(version)

        return version


    def get_archived_versions(
        self,
        db: Session,
        section_id: int,
    ) -> list[Version]:
        """
        Retrieve archived versions of a section.
        """

        return self.repository.get_archived_versions(
            db,
            section_id,
        )