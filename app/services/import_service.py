"""
Import service.

Handles DOCX files re-imported after external editing
in Microsoft Word.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.models.section import Section
from app.repositories.section_repository import SectionRepository
from app.services.permission_service import PermissionService
from app.services.storage_service import StorageService
from app.word.parser import DocxParser
from app.services.word_comparison_service import (
    WordComparisonService,
)
from app.enums.section_status import SectionStatus
from app.services.version_service import VersionService
from app.services.validation_service import ValidationService


class ImportService:
    """
    Service responsible for importing externally edited DOCX files.
    """

    def __init__(self):
        self.section_repository = SectionRepository()
        self.storage_service = StorageService()
        self.parser = DocxParser()
        self.comparison_service = WordComparisonService()
        self.version_service = VersionService()

    def import_section(
        self,
        db: Session,
        section_id: int,
        user_id: int,
        file,
    ) -> dict:
        """
        Import an externally edited DOCX section.

        This method:
        1. checks section access
        2. stores the uploaded DOCX
        3. parses the DOCX
        4. compares it with the current section
        5. returns the comparison result

        No version is created here.
        """

        # ==================================================
        # GET SECTION
        # ==================================================

        section = (
            self.section_repository.get_section_by_id(
                db,
                section_id,
            )
        )

        if section is None:
            return None

        # ==================================================
        # PERMISSION
        # ==================================================

        PermissionService.check_section_editor(
            db,
            section,
            user_id,
        )

        # ==================================================
        # VALIDATE FILE
        # ==================================================

        if not file.filename:
            raise ValueError(
                "A DOCX file is required."
            )

        extension = Path(
            file.filename
        ).suffix.lower()

        if extension != ".docx":
            raise ValueError(
                "Only .docx files are allowed."
            )

        # ==================================================
        # SAVE FILE
        # ==================================================

        storage_key = self.storage_service.save_file(
            file
        )

        absolute_path = (
            self.storage_service.get_absolute_path(
                storage_key
            )
        )

        # ==================================================
        # PARSE DOCX
        # ==================================================

        imported_data = self.parser.parse(
            absolute_path,
            expected_title=section.title,
        )

        # ==================================================
        # COMPARE
        # ==================================================

        comparison = self.comparison_service.compare(
            current_title=section.title,
            current_content=section.content or "",
            imported_title=imported_data["title"],
            imported_content=imported_data["content"],
        )

        # ==================================================
        # RESULT
        # ==================================================

        result = {
            "section_id": section.id,
            "storage_key": storage_key,
            "changed": comparison["changed"],
            "title_changed": comparison["title_changed"],
            "content_changed": comparison["content_changed"],
            "current_title": comparison["current_title"],
            "imported_title": comparison["imported_title"],
            "current_content": comparison["current_content"],
            "imported_content": comparison["imported_content"],
        }

        # ==================================================
        # NO CHANGE
        # ==================================================

        if not comparison["changed"]:
            return result

        # ==================================================
        # CREATE PROPOSED VERSION
        # ==================================================

        version = self.version_service.create_new_version(
            db=db,
            section_id=section.id,
            author_id=user_id,
            title_snapshot=imported_data["title"],
            content_snapshot=imported_data["content"],
            change_comment="Imported modification from Microsoft Word",
            make_current=False,
            storage_key=storage_key,
        )

        # ==================================================
        # SECTION → PENDING VALIDATION
        # ==================================================

        section.status = SectionStatus.PENDING_VALIDATION

        # ==================================================
        # CREATE VALIDATION
        # ==================================================

        validation = ValidationService.create_validation(
            db=db,
            version_id=version.id,
        )

        db.commit()
        db.refresh(section)
        db.refresh(version)
        db.refresh(validation)

        # ==================================================
        # RESULT WITH VERSION + VALIDATION
        # ==================================================

        result.update(
            {
                "version_id": version.id,
                "validation_id": validation.id,
                "version_is_current": version.is_current,
                "section_status": section.status,
            }
        )

        return result