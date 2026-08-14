"""
Validation repository.

This module contains database access logic
related to section version validations.
"""

from sqlalchemy.orm import Session

from app.models.validation import Validation


class ValidationRepository:
    """
    Repository responsible for validation persistence.
    """

    @staticmethod
    def create(
        db: Session,
        validation: Validation,
    ) -> Validation:
        """
        Create a new validation.
        """

        db.add(validation)
        db.commit()
        db.refresh(validation)

        return validation

    @staticmethod
    def get_by_id(
        db: Session,
        validation_id: int,
    ) -> Validation | None:
        """
        Retrieve a validation by its ID.
        """

        return (
            db.query(Validation)
            .filter(
                Validation.id == validation_id
            )
            .first()
        )

    @staticmethod
    def get_by_version_id(
        db: Session,
        version_id: int,
    ) -> Validation | None:
        """
        Retrieve the validation associated
        with a specific version.
        """

        return (
            db.query(Validation)
            .filter(
                Validation.version_id == version_id
            )
            .first()
        )

    @staticmethod
    def get_by_section_id(
        db: Session,
        section_id: int,
    ) -> list[Validation]:
        """
        Retrieve all validations associated
        with versions of a section.
        """

        return (
            db.query(Validation)
            .join(Validation.version)
            .filter(
                Validation.version.has(
                    section_id=section_id
                )
            )
            .order_by(
                Validation.id.desc()
            )
            .all()
        )


    @staticmethod
    def update(
        db: Session,
        validation: Validation,
    ) -> Validation:
        """
        Update an existing validation.
        """

        db.commit()
        db.refresh(validation)

        return validation

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Validation]:
        """
        Retrieve all validations.
        """

        return (
            db.query(Validation)
            .order_by(
                Validation.id.desc()
            )
            .all()
        )