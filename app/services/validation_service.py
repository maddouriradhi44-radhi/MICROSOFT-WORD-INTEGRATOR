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

from app.enums.section_status import SectionStatus

from app.repositories.version_repository import VersionRepository
from app.repositories.section_repository import SectionRepository

from app.models.document_block import DocumentBlock
from app.repositories.document_block_repository import (
    DocumentBlockRepository,
)

from app.services.storage_service import StorageService
from app.services.docx_analyzer_service import DocxAnalyzerService

from app.services.ai.ai_validation_report_service import (
    AIValidationReportService,
)

from app.services.ai.ai_validation_decision_service import (
    AIValidationDecisionService,
)

from app.repositories.project_member_repository import (
    ProjectMemberRepository,
)

from app.word.parser import DocxParser


class ValidationService:
    """
    Service responsible for validation business logic.
    """

    notification_service = NotificationService()
    audit_service = AuditLogService()

    version_repository = VersionRepository()
    section_repository = SectionRepository()
    document_block_repository = DocumentBlockRepository()

    storage_service = StorageService()
    analyzer_service = DocxAnalyzerService()
    parser = DocxParser()

    ai_report_service = AIValidationReportService()
    ai_decision_service = AIValidationDecisionService()



    # ======================================================
    # INTERNAL HELPER
    # ======================================================

    @staticmethod
    def _find_analyzed_section(
        analyzed_sections: list[dict],
        version: Version,
    ) -> dict | None:
        """
        Find the section corresponding to the approved version
        inside the analyzed DOCX.

        Priority:
        1. If the DOCX contains only one section, use it.
        2. Otherwise try to match the version title.
        3. If no exact match exists, try normalized comparison.

        This is necessary because the collaborator can rename
        the Heading 1 in Microsoft Word.

        Example:

            version.title_snapshot = "string"
            DOCX Heading 1 = "Introduction"

        In this case, "Introduction" must be considered
        the real approved section title.
        """

        if not analyzed_sections:
            return None

        # --------------------------------------------------
        # CASE 1: DOCX contains exactly one section
        # --------------------------------------------------

        if len(analyzed_sections) == 1:
            return analyzed_sections[0]

        # --------------------------------------------------
        # CASE 2: Exact title comparison
        # --------------------------------------------------

        version_title = (
            version.title_snapshot.strip()
            if version.title_snapshot
            else ""
        )

        for analyzed in analyzed_sections:

            analyzed_title = (
                analyzed.get("title", "").strip()
            )

            if (
                analyzed_title
                and analyzed_title == version_title
            ):
                return analyzed

        # --------------------------------------------------
        # CASE 3: Normalized comparison
        # --------------------------------------------------

        normalized_version_title = " ".join(
            version_title.lower().split()
        )

        for analyzed in analyzed_sections:

            analyzed_title = (
                analyzed.get("title", "").strip()
            )

            normalized_analyzed_title = " ".join(
                analyzed_title.lower().split()
            )

            if (
                normalized_analyzed_title
                and normalized_analyzed_title
                == normalized_version_title
            ):
                return analyzed

        return None

    # ======================================================
    # INTERNAL HELPER
    # ======================================================

    @staticmethod
    def _apply_approved_version(
        db: Session,
        version: Version,
    ) -> None:
        """
        Apply an approved version to the section.

        Responsibilities:
        - make the version current
        - deactivate the previous current version
        - analyze the approved DOCX
        - update DocumentBlocks
        - update section title/content
        - mark section as VALIDATED
        """

        # ==================================================
        # MAKE VERSION OFFICIAL
        # ==================================================

        current_version = (
            ValidationService.version_repository
            .get_current_version(
                db,
                version.section_id,
            )
        )

        if (
            current_version is not None
            and current_version.id != version.id
        ):
            current_version.is_current = False

        version.is_current = True

        # ==================================================
        # GET SECTION
        # ==================================================

        section = (
            ValidationService.section_repository
            .get_section_by_id(
                db,
                version.section_id,
            )
        )

        if section is None:
            raise ValueError("Section not found")

        # ==================================================
        # UPDATE DOCUMENT BLOCKS FROM APPROVED DOCX
        # ==================================================

        approved_title = version.title_snapshot
        approved_content = version.content_snapshot

        if version.storage_key:

            docx_path = (
                ValidationService.storage_service
                .get_absolute_path(
                    version.storage_key
                )
            )

            if not docx_path.exists():
                raise ValueError(
                    "Approved DOCX file not found"
                )

            parsed_data = (
                ValidationService.parser.parse(
                    docx_path,
                    expected_title=version.title_snapshot,
                )
            )

            approved_title = parsed_data["title"]
            approved_content = parsed_data["content"]

            # --------------------------------------------------
            # ANALYZE DOCX
            # --------------------------------------------------

            analyzed_sections = (
                ValidationService.analyzer_service
                .analyze(
                    str(docx_path)
                )
            )

            # --------------------------------------------------
            # FIND THE APPROVED SECTION
            # --------------------------------------------------

            analyzed_section = (
                ValidationService._find_analyzed_section(
                    analyzed_sections,
                    version,
                )
            )

            if analyzed_section is None:
                raise ValueError(
                    "Approved section not found in DOCX"
                )
            # --------------------------------------------------
            # USE ANALYZED CONTENT WHEN AVAILABLE
            # --------------------------------------------------

            analyzed_content = (
                analyzed_section.get("content")
            )

            if analyzed_content is not None:
                approved_content = analyzed_content

            # --------------------------------------------------
            # DELETE OLD BLOCKS
            # --------------------------------------------------

            ValidationService.document_block_repository \
                .delete_section_blocks(
                    db,
                    version.section_id,
                )

            # --------------------------------------------------
            # CREATE NEW BLOCKS
            # --------------------------------------------------

            for block_data in (
                analyzed_section.get("blocks", [])
            ):

                block = DocumentBlock(
                    section_id=version.section_id,
                    type=block_data["type"],
                    content_xml=block_data["content_xml"],
                    order_index=block_data["order_index"],
                )

                db.add(block)

            db.flush()

        # ==================================================
        # UPDATE VERSION SNAPSHOT
        # ==================================================

        version.title_snapshot = approved_title
        version.content_snapshot = approved_content

        # ==================================================
        # UPDATE SECTION
        # ==================================================

        section.title = approved_title
        section.content = approved_content
        section.status = SectionStatus.VALIDATED

        db.flush()

    # ======================================================
    # CREATE VALIDATION
    # ======================================================

    @staticmethod
    def create_validation(
        db: Session,
        version_id: int,
    ) -> Validation:
        """
        Create a validation and let the AI determine whether
        the version can be automatically validated.

        Non-critical modifications are automatically validated
        by AI.

        Critical modifications remain pending and are sent
        to the Project Manager for manual review.
        """

        # ==================================================
        # GET VERSION
        # ==================================================

        version = (
            db.query(Version)
            .filter(
                Version.id == version_id
            )
            .first()
        )

        if version is None:
            raise ValueError("Version not found")

        # ==================================================
        # CHECK EXISTING VALIDATION
        # ==================================================

        existing_validation = (
            ValidationRepository.get_by_version_id(
                db,
                version_id,
            )
        )

        if existing_validation:
            return existing_validation

        # ==================================================
        # CREATE PENDING VALIDATION
        # ==================================================

        validation = Validation(
            version_id=version_id,
            status=ValidationStatus.PENDING,
            validated_by_ai=False,
        )

        validation = ValidationRepository.create(
            db,
            validation,
        )

        # ==================================================
        # GENERATE AI REPORT
        # ==================================================

        report = (
            ValidationService.ai_report_service
            .generate_report(
                db,
                validation,
            )
        )

        # ==================================================
        # AI DECISION
        # ==================================================

        can_auto_validate = (
            ValidationService.ai_decision_service
            .can_auto_validate(
                report
            )
        )

        # ==================================================
        # AUTOMATIC AI VALIDATION
        # ==================================================

        if can_auto_validate:

            validation.status = (
                ValidationStatus.APPROVED
            )

            validation.validated_by_ai = True

            validation.validated_at = (
                datetime.utcnow()
            )

            validation.comment = (
                report.recommendation_reason
            )

            # --------------------------------------------------
            # APPLY APPROVED VERSION
            # --------------------------------------------------

            ValidationService._apply_approved_version(
                db,
                version,
            )

            # --------------------------------------------------
            # NOTIFY COLLABORATOR
            # --------------------------------------------------

            ValidationService.notification_service \
                .notify_user(
                    db=db,
                    user_id=version.author_id,
                    title="Validation automatique par l'IA",
                    message=(
                        f"La version "
                        f"{version.version_number} "
                        "de votre section a été "
                        "validée automatiquement "
                        "par l'IA."
                    ),
                    notification_type=(
                        NotificationType.VALIDATION
                    ),
                    level=(
                        NotificationLevel.SUCCESS
                    ),
                    entity_type="validation",
                    entity_id=validation.id,
                )

            # --------------------------------------------------
            # AUDIT
            # --------------------------------------------------

            ValidationService.audit_service.log_action(
                db=db,
                user_id=version.author_id,
                action=AuditAction.CREATE,
                target=(
                    f"AI validation "
                    f"{validation.id} "
                    f"for Version {version.id}"
                ),
            )

            return ValidationRepository.update(
                db,
                validation,
            )

        # ==================================================
        # PROJECT MANAGER REVIEW REQUIRED
        # ==================================================

        project_manager = (
            ProjectMemberRepository
            .get_project_manager(
                db,
                version.section.project_id,
            )
        )

        # ==================================================
        # NOTIFY PROJECT MANAGER
        # ==================================================

        if project_manager is not None:

            ValidationService.notification_service \
                .notify_user(
                    db=db,
                    user_id=project_manager.user_id,
                    title="Validation requise",
                    message=(
                        f"La version "
                        f"{version.version_number} "
                        "de votre section nécessite "
                        "une validation manuelle. "
                        "L'analyse IA recommande une "
                        "vérification avant validation."
                    ),
                    notification_type=(
                        NotificationType.VALIDATION
                    ),
                    level=(
                        NotificationLevel.WARNING
                    ),
                    entity_type="validation",
                    entity_id=validation.id,
                )

        # ==================================================
        # AUDIT
        # ==================================================

        ValidationService.audit_service.log_action(
            db=db,
            user_id=version.author_id,
            action=AuditAction.CREATE,
            target=(
                f"Validation "
                f"{validation.id} "
                f"for Version {version.id}"
            ),
        )

        return validation

    # ======================================================
    # GET VALIDATION BY VERSION
    # ======================================================

    @staticmethod
    def get_validation_by_version(
        db: Session,
        version_id: int,
    ) -> Validation | None:
        """
        Retrieve the validation associated with a version.
        """

        return (
            ValidationRepository.get_by_version_id(
                db,
                version_id,
            )
        )

    # ======================================================
    # VALIDATION HISTORY
    # ======================================================

    @staticmethod
    def get_validation_history(
        db: Session,
        section_id: int,
    ) -> list[Validation]:
        """
        Retrieve validation history for a section.
        """

        return (
            ValidationRepository.get_by_section_id(
                db,
                section_id,
            )
        )

    # ======================================================
    # APPROVE VALIDATION
    # ======================================================

    @staticmethod
    def approve_validation(
        db: Session,
        validation_id: int,
        reviewer_id: int,
        comment: str | None = None,
    ) -> Validation:
        """
        Approve a pending validation manually
        by the Project Manager.
        """

        # ==================================================
        # GET VALIDATION
        # ==================================================

        validation = (
            ValidationRepository.get_by_id(
                db,
                validation_id,
            )
        )

        if validation is None:
            raise ValueError(
                "Validation not found"
            )

        # ==================================================
        # CHECK STATUS
        # ==================================================

        if validation.status != (
            ValidationStatus.PENDING
        ):
            raise ValueError(
                "Only pending validations can be approved"
            )

        # ==================================================
        # GET VERSION
        # ==================================================

        version = validation.version

        if version is None:
            raise ValueError(
                "Version not found"
            )

        # ==================================================
        # UPDATE VALIDATION
        # ==================================================

        validation.status = (
            ValidationStatus.APPROVED
        )

        validation.reviewer_id = reviewer_id

        validation.comment = comment

        validation.validated_at = (
            datetime.utcnow()
        )

        validation.validated_by_ai = False

        # ==================================================
        # APPLY APPROVED VERSION
        # ==================================================

        ValidationService._apply_approved_version(
            db,
            version,
        )

        # ==================================================
        # NOTIFY COLLABORATOR
        # ==================================================

        ValidationService.notification_service \
            .notify_user(
                db=db,
                user_id=version.author_id,
                title="Validation approuvée",
                message=(
                    f"La version "
                    f"{version.version_number} "
                    "de votre section a été approuvée."
                ),
                notification_type=(
                    NotificationType.VALIDATION
                ),
                level=(
                    NotificationLevel.SUCCESS
                ),
                entity_type="validation",
                entity_id=validation.id,
            )

        # ==================================================
        # AUDIT
        # ==================================================

        ValidationService.audit_service.log_action(
            db=db,
            user_id=reviewer_id,
            action=AuditAction.CREATE,
            target=(
                f"Validation "
                f"{validation.id} "
                f"for Version "
                f"{validation.version_id}"
            ),
        )

        return ValidationRepository.update(
            db,
            validation,
        )

    # ======================================================
    # REJECT VALIDATION
    # ======================================================

    @staticmethod
    def reject_validation(
        db: Session,
        validation_id: int,
        reviewer_id: int,
        comment: str,
    ) -> Validation:
        """
        Reject a pending validation manually
        by the Project Manager.
        """

        # ==================================================
        # GET VALIDATION
        # ==================================================

        validation = (
            ValidationRepository.get_by_id(
                db,
                validation_id,
            )
        )

        if validation is None:
            raise ValueError(
                "Validation not found"
            )

        # ==================================================
        # CHECK STATUS
        # ==================================================

        if validation.status != (
            ValidationStatus.PENDING
        ):
            raise ValueError(
                "Only pending validations can be rejected"
            )

        # ==================================================
        # UPDATE VALIDATION
        # ==================================================

        validation.status = (
            ValidationStatus.REJECTED
        )

        validation.reviewer_id = reviewer_id

        validation.comment = comment

        validation.validated_at = (
            datetime.utcnow()
        )

        validation.validated_by_ai = False

        # ==================================================
        # GET VERSION
        # ==================================================

        version = validation.version

        if version is None:
            raise ValueError(
                "Version not found"
            )

        # ==================================================
        # SECTION → REJECTED
        # ==================================================

        section = (
            ValidationService.section_repository
            .get_section_by_id(
                db,
                version.section_id,
            )
        )

        if section is not None:
            section.status = (
                SectionStatus.REJECTED
            )

        # ==================================================
        # SAVE VALIDATION
        # ==================================================

        validation = (
            ValidationRepository.update(
                db,
                validation,
            )
        )

        # ==================================================
        # NOTIFY COLLABORATOR
        # ==================================================

        ValidationService.notification_service \
            .notify_user(
                db=db,
                user_id=version.author_id,
                title="Validation refusée",
                message=(
                    f"La version "
                    f"{version.version_number} "
                    "de votre section a été refusée. "
                    f"Commentaire : {validation.comment}"
                ),
                notification_type=(
                    NotificationType.VALIDATION
                ),
                level=(
                    NotificationLevel.WARNING
                ),
                entity_type="validation",
                entity_id=validation.id,
            )

        # ==================================================
        # AUDIT
        # ==================================================

        ValidationService.audit_service.log_action(
            db=db,
            user_id=reviewer_id,
            action=AuditAction.REJECT,
            target=(
                f"Validation "
                f"{validation.id} "
                f"for Version "
                f"{validation.version_id}"
            ),
        )

        return validation