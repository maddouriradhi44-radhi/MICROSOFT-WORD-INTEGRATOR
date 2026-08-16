"""
DOCX export service.

Handles business logic related to document export.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.repositories.document_block_repository import DocumentBlockRepository
from app.services.permission_service import PermissionService
from app.services.storage_service import StorageService
from app.word.exporter import DocxExporter
from app.repositories.section_repository import SectionRepository


class ExportService:
    """
    Business logic responsible for exporting documents to DOCX.
    """

    def __init__(self):
        self.document_repository = DocumentRepository()
        self.block_repository = DocumentBlockRepository()
        self.storage_service = StorageService()
        self.exporter = DocxExporter()
        self.section_repository = SectionRepository()

    def export_document(
        self,
        db: Session,
        document_id: int,
        user_id: int,
        output_path: str | Path,
    ) -> Path:
        """
        Export a complete document using its stored sections
        and document blocks.
        """

        # ======================================================
        # GET DOCUMENT
        # ======================================================

        document = self.document_repository.get_document_by_id(
            db,
            document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        # ======================================================
        # CHECK PROJECT ACCESS
        # ======================================================

        PermissionService.get_project_member(
            db,
            document.project_id,
            user_id,
        )

        # ======================================================
        # CHECK ORIGINAL FILE
        # ======================================================

        if not document.storage_key:
            raise HTTPException(
                status_code=404,
                detail="Original document file not found",
            )

        original_path = (
            self.storage_service.get_absolute_path(
                document.storage_key
            )
        )

        if not original_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Original document file not found",
            )

        # ======================================================
        # GET SECTIONS
        # ======================================================

        sections = sorted(
            document.sections,
            key=lambda section: section.order,
        )

        # ======================================================
        # COLLECT BLOCKS
        # ======================================================

        blocks = []

        for section in sections:

            section_blocks = (
                self.block_repository.get_section_blocks(
                    db,
                    section.id,
                )
            )

            blocks.extend(section_blocks)

        # ======================================================
        # VALIDATE CONTENT
        # ======================================================

        if not blocks:
            raise HTTPException(
                status_code=400,
                detail="Document contains no blocks to export",
            )

        # ======================================================
        # EXPORT DOCX
        # ======================================================

        return self.exporter.export(
            original_path=original_path,
            output_path=output_path,
            blocks=blocks,
        )

    def export_section(
        self,
        db: Session,
        section_id: int,
        user_id: int,
        output_path: str | Path,
    ) -> Path:
        """
        Export a single section to a DOCX file.

        Only project managers and collaborators assigned
        to the section can export it for external editing.
        """

        # ======================================================
        # GET SECTION
        # ======================================================

        section = self.section_repository.get_section_by_id(
            db,
            section_id,
        )

        if section is None:
            raise HTTPException(
                status_code=404,
                detail="Section not found",
            )

        # ======================================================
        # CHECK SECTION EDITOR ACCESS
        # ======================================================

        PermissionService.check_section_editor(
            db,
            section,
            user_id,
        )

        # ======================================================
        # GET DOCUMENT
        # ======================================================

        document = self.document_repository.get_document_by_id(
            db,
            section.document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        # ======================================================
        # CHECK ORIGINAL FILE
        # ======================================================

        if not document.storage_key:
            raise HTTPException(
                status_code=404,
                detail="Original document file not found",
            )

        original_path = (
            self.storage_service.get_absolute_path(
                document.storage_key
            )
        )

        if not original_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Original document file not found",
            )

        # ======================================================
        # GET SECTION BLOCKS
        # ======================================================

        blocks = self.block_repository.get_section_blocks(
            db,
            section.id,
        )

        # ======================================================
        # VALIDATE CONTENT
        # ======================================================

        if not blocks:
            raise HTTPException(
                status_code=400,
                detail="Section contains no blocks to export",
            )

        # ======================================================
        # EXPORT SECTION
        # ======================================================

        return self.exporter.export(
            original_path=original_path,
            output_path=output_path,
            blocks=blocks,
        )
