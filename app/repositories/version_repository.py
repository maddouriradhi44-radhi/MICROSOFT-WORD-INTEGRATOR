"""
Version repository.

This module handles database operations
related to document section versions.
"""

from sqlalchemy.orm import Session

from app.models.version import Version


class VersionRepository:
    """
    Repository responsible for Version database operations.
    """

    def create_version(
        self,
        db: Session,
        version: Version,
    ) -> Version:
        """
        Create a new version.
        """

        db.add(version)

        db.commit()

        db.refresh(version)

        return version


    def get_version_by_id(
        self,
        db: Session,
        version_id: int,
    ) -> Version | None:
        """
        Retrieve a version by id.
        """

        return (
            db.query(Version)
            .filter(
                Version.id == version_id
            )
            .first()
        )


    def get_section_versions(
        self,
        db: Session,
        section_id: int,
    ) -> list[Version]:
        """
        Retrieve the complete history
        of a section.
        """

        return (
            db.query(Version)
            .filter(
                Version.section_id == section_id
            )
            .order_by(
                Version.version_number.asc()
            )
            .all()
        )


    def get_current_version(
        self,
        db: Session,
        section_id: int,
    ) -> Version | None:
        """
        Retrieve the active version
        of a section.
        """

        return (
            db.query(Version)
            .filter(
                Version.section_id == section_id,
                Version.is_current.is_(True)
            )
            .first()
        )


    def get_latest_version_number(
        self,
        db: Session,
        section_id: int,
    ) -> int:
        """
        Get the latest version number
        for a section.
        """

        version = (
            db.query(Version)
            .filter(
                Version.section_id == section_id
            )
            .order_by(
                Version.version_number.desc()
            )
            .first()
        )

        if version is None:
            return 0

        return version.version_number


    def archive_version(
        self,
        db: Session,
        version: Version,
    ) -> Version:
        """
        Archive a version without deleting it.
        """

        version.is_archived = True

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

        return (
            db.query(Version)
            .filter(
                Version.section_id == section_id,
                Version.is_archived.is_(True),
            )
            .order_by(
                Version.version_number.asc()
            )
            .all()
        )