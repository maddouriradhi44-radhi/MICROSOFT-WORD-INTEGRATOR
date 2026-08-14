"""
Validation service.

This module contains the business logic
related to section version validations.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.validation import Validation
from app.repositories.validation_repository import ValidationRepository
from app.enums.validation_status import ValidationStatus
from app.models.version import Version
from app.services.notifications_service import NotificationService
from app.enums.notification_type import NotificationType
from app.enums.notification_level import NotificationLevel
from app.services.audit_log_service import AuditLogService
from app.enums.audit_action import AuditAction


class ValidationService:
    """
    Service responsible for validation business logic.
    """
    notification_service = NotificationService()
    audit_service = AuditLogService()
    @staticmethod
    def create_validation(
        db: Session,
        version_id: int,
    ) -> Validation:
        """
        Create a pending validation for a version.
        """
        version = (
            db.query(Version)
            .filter(
            Version.id == version_id
        )
        .first()
)

        if version is None:
            raise ValueError("Version not found")
        existing_validation = (
            ValidationRepository.get_by_version_id(
                db,
                version_id,
            )
        )

        if existing_validation:
            return existing_validation

        validation = Validation(
            version_id=version_id,
            status=ValidationStatus.PENDING,
            validated_by_ai=False,
        )

        validation = ValidationRepository.create(
            db,
            validation,
        )

        ValidationService.notification_service.notify_user(
            db=db,
            user_id=version.author_id,
            title="Validation requise",
            message=f"La version {version.version_number} de votre section a été envoyée pour validation.",
            notification_type=NotificationType.VALIDATION,
            level=NotificationLevel.INFO,
            entity_type="validation",
            entity_id=validation.id,
        )

        ValidationService.audit_service.log_action(
            db=db,
            user_id=version.author_id,
            action=AuditAction.CREATE,
            target=f"Validation {validation.id} for Version {version.id}",
        )

        return validation

    @staticmethod
    def get_validation_by_version(
        db: Session,
        version_id: int,
    ) -> Validation | None:
        """
        Retrieve the validation associated with a version.
        """

        return ValidationRepository.get_by_version_id(
            db,
            version_id,
        )

    @staticmethod
    def get_validation_history(
        db: Session,
        section_id: int,
    ) -> list[Validation]:
        """
        Retrieve validation history for a section.
        """

        return ValidationRepository.get_by_section_id(
            db,
            section_id,
        )


    @staticmethod
    def approve_validation(
        db: Session,
        validation_id: int,
        reviewer_id: int,
        comment: str | None = None,
    ) -> Validation:
        """
        Approve a validation.
        """

        validation = ValidationRepository.get_by_id(
            db,
            validation_id,
        )

        if validation is None:
            raise ValueError("Validation not found")

        if validation.status != ValidationStatus.PENDING:
            raise ValueError(
                "Only pending validations can be approved"
            )

        validation.status = ValidationStatus.APPROVED
        validation.reviewer_id = reviewer_id
        validation.comment = comment
        validation.validated_at = datetime.utcnow()
        validation.validated_by_ai = False

        ValidationService.notification_service.notify_user(
            db=db,
            user_id=validation.version.author_id,
            title="Validation approuvée",
            message=f"La version {validation.version.version_number} de votre section a été approuvée.",
            notification_type=NotificationType.VALIDATION,
            level=NotificationLevel.SUCCESS,
            entity_type="validation",
            entity_id=validation.id,
        )

        return ValidationRepository.update(
            db,
            validation,
        )

    @staticmethod
    def reject_validation(
        db: Session,
        validation_id: int,
        reviewer_id: int,
        comment: str,
    ) -> Validation:
        """
        Reject a validation.
        """

        validation = ValidationRepository.get_by_id(
            db,
            validation_id,
        )

        if validation is None:
            raise ValueError("Validation not found")

        if validation.status != ValidationStatus.PENDING:
            raise ValueError(
                "Only pending validations can be rejected"
            )

        validation.status = ValidationStatus.REJECTED
        validation.reviewer_id = reviewer_id
        validation.comment = comment
        validation.validated_at = datetime.utcnow()
        validation.validated_by_ai = False

        validation = ValidationRepository.update(
            db,
            validation,
        )

        ValidationService.notification_service.notify_user(
            db=db,
            user_id=validation.version.author_id,
            title="Validation refusée",
            message=f"La version {validation.version.version_number} de votre section a été refusée. Commentaire : {validation.comment}",
            notification_type=NotificationType.VALIDATION,
            level=NotificationLevel.WARNING,
            entity_type="validation",
            entity_id=validation.id,
        )

        ValidationService.audit_service.log_action(
            db=db,
            user_id=reviewer_id,
            action=AuditAction.REJECT,
            target=f"Validation {validation.id} for Version {validation.version_id}",
        )

        return validation