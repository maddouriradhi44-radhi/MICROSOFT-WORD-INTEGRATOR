from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_lock import DocumentLock

from app.repositories.document_repository import DocumentRepository
from app.repositories.document_lock_repository import DocumentLockRepository
from app.repositories.project_member_repository import ProjectMemberRepository

from app.schemas.document_schema import (
    DocumentCreate,
    DocumentUpdate,
)

from app.services.permission_service import PermissionService
from app.services.storage_service import StorageService
from app.services.docx_analyzer_service import DocxAnalyzerService
from app.services.section_service import SectionService
from app.services.notifications_service import NotificationService

from app.enums.notification_level import NotificationLevel
from app.enums.notification_type import NotificationType


class DocumentService:
    """
    Business logic related to documents.
    """

    def __init__(self):
        self.repository = DocumentRepository()
        self.lock_repository = DocumentLockRepository()

    # ==========================================================
    # CREATE DOCUMENT
    # ==========================================================

    def create_document(
        self,
        db: Session,
        document_data: DocumentCreate,
        owner_id: int,
        storage_key: str,
        original_filename: str,
    ) -> Document:
        """
        Create and persist a new document.
        """

        PermissionService.check_project_manager(
            db,
            document_data.project_id,
            owner_id,
        )

        document = Document(
            title=document_data.title,
            original_filename=original_filename,
            storage_key=storage_key,
            owner_id=owner_id,
            project_id=document_data.project_id,
        )

        created_document = self.repository.create_document(
            db,
            document,
        )

        # ======================================================
        # ANALYZE DOCUMENT
        # ======================================================

        storage_service = StorageService()

        absolute_path = storage_service.get_absolute_path(
            created_document.storage_key
        )

        analyzer = DocxAnalyzerService()

        sections = analyzer.analyze(
            absolute_path
        )

        # ======================================================
        # CREATE SECTIONS
        # ======================================================

        section_service = SectionService()

        section_service.create_sections(
            db,
            created_document.id,
            created_document.project_id,
            sections,
        )

        # ======================================================
        # NOTIFY PROJECT MEMBERS
        # ======================================================

        members = ProjectMemberRepository.get_project_members(
            db,
            created_document.project_id,
        )

        notification_service = NotificationService()

        for member in members:
            notification_service.notify_user(
                db=db,
                user_id=member.user_id,
                title="Nouveau document",
                message=(
                    f"Le document « {created_document.title} » "
                    f"a été ajouté au projet."
                ),
                notification_type=NotificationType.DOCUMENT,
                level=NotificationLevel.INFO,
                entity_type="document",
                entity_id=created_document.id,
            )

        return created_document

    # ==========================================================
    # ATTACH DOCUMENT TO PROJECT
    # ==========================================================

    def attach_to_project(
        self,
        db: Session,
        document_id: int,
        project_id: int,
    ) -> Document | None:

        document = self.repository.get_document_by_id(
            db,
            document_id,
        )

        if document is None:
            return None

        return self.repository.update_document(
            db,
            document,
            {
                "project_id": project_id
            },
        )

    # ==========================================================
    # VERIFY PROJECT OWNER
    # ==========================================================

    def verify_project_owner(
        self,
        db: Session,
        project_id: int,
        user_id: int,
    ) -> bool:

        PermissionService.check_project_manager(
            db,
            project_id,
            user_id,
        )

        return True

    # ==========================================================
    # PREPARE DOCX IMPORT
    # ==========================================================

    def prepare_docx_import(
        self,
        file_path: str,
    ) -> None:
        """
        Placeholder for future DOCX import.
        """

        pass

    # ==========================================================
    # GET DOCUMENT BY ID
    # ==========================================================

    def get_document_by_id(
        self,
        db: Session,
        document_id: int,
    ) -> Document | None:

        return self.repository.get_document_by_id(
            db,
            document_id,
        )

    # ==========================================================
    # GET PROJECT DOCUMENTS
    # ==========================================================

    def get_project_documents(
        self,
        db: Session,
        project_id: int,
    ) -> list[Document]:

        return self.repository.get_project_documents(
            db,
            project_id,
        )

    # ==========================================================
    # UPDATE DOCUMENT
    # ==========================================================

    def update_document(
        self,
        db: Session,
        document_id: int,
        document_data: DocumentUpdate,
        user_id: int,
    ) -> Document | None:
        """
        Update document safely using lock system.

        All project members are notified after the modification.
        """

        # ======================================================
        # GET DOCUMENT
        # ======================================================

        document = self.repository.get_document_by_id(
            db,
            document_id,
        )

        if document is None:
            return None

        # ======================================================
        # CHECK PERMISSION
        # ======================================================

        PermissionService.check_project_manager(
            db,
            document.project_id,
            user_id,
        )

        # ======================================================
        # CHECK EXISTING LOCK
        # ======================================================

        existing_lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        # Locked by another user
        if existing_lock and existing_lock.user_id != user_id:
            raise HTTPException(
                status_code=423,
                detail="Document is currently locked by another user",
            )

        # ======================================================
        # PREPARE UPDATES
        # ======================================================

        updates = document_data.model_dump(
            exclude_unset=True
        )

        temporary_lock = False

        # ======================================================
        # CREATE TEMPORARY LOCK
        # ======================================================

        if existing_lock is None:

            self.create_document_lock(
                db,
                document_id,
                user_id,
            )

            temporary_lock = True

        try:

            # ==================================================
            # UPDATE DOCUMENT
            # ==================================================

            updated_document = self.repository.update_document(
                db,
                document,
                updates,
            )

            # ==================================================
            # NOTIFY ALL PROJECT MEMBERS
            # ==================================================

            members = ProjectMemberRepository.get_project_members(
                db,
                document.project_id,
            )

            notification_service = NotificationService()

            for member in members:
                notification_service.notify_user(
                    db=db,
                    user_id=member.user_id,
                    title="Document modifié",
                    message=(
                        f"Le document « {updated_document.title} » "
                        f"a été modifié."
                    ),
                    notification_type=NotificationType.DOCUMENT,
                    level=NotificationLevel.INFO,
                    entity_type="document",
                    entity_id=updated_document.id,
                )

        finally:

            # ==================================================
            # RELEASE TEMPORARY LOCK
            # ==================================================

            if temporary_lock:

                self.release_document_lock(
                    db,
                    document_id,
                )

        return updated_document

    # ==========================================================
    # DELETE DOCUMENT
    # ==========================================================

    def delete_document(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> bool:
        """
        Delete a document and notify all project members.

        Only the PROJECT_MANAGER can delete the document.
        """

        # ======================================================
        # GET DOCUMENT
        # ======================================================

        document = self.repository.get_document_by_id(
            db,
            document_id,
        )

        if document is None:
            return False

        # ======================================================
        # CHECK PERMISSION
        # ======================================================

        PermissionService.check_project_manager(
            db,
            document.project_id,
            user_id,
        )

        # ======================================================
        # SAVE INFORMATION BEFORE DELETION
        # ======================================================

        document_title = document.title
        project_id = document.project_id

        # ======================================================
        # GET PROJECT MEMBERS BEFORE DELETION
        # ======================================================

        members = ProjectMemberRepository.get_project_members(
            db,
            project_id,
        )

        # ======================================================
        # DELETE DOCUMENT
        # ======================================================

        self.repository.delete_document(
            db,
            document,
        )

        # ======================================================
        # NOTIFY ALL PROJECT MEMBERS
        # ======================================================

        notification_service = NotificationService()

        for member in members:
            notification_service.notify_user(
                db=db,
                user_id=member.user_id,
                title="Document Deleted",
                message=(
                    f"The document '{document_title}' "
                    f"has been deleted from the project."
                ),
                notification_type=NotificationType.DOCUMENT,
                level=NotificationLevel.WARNING,
                entity_type="document",
                entity_id=document_id,
            )

        return True

    
    # ==========================================================
    # CREATE DOCUMENT LOCK
    # ==========================================================

    def create_document_lock(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> DocumentLock:
        """
        Create document lock and notify the user.
        """

        # ======================================================
        # CHECK EXISTING LOCK
        # ======================================================

        existing_lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        if existing_lock:
            raise HTTPException(
                status_code=423,
                detail="Document is currently locked",
            )

        # ======================================================
        # GET DOCUMENT
        # ======================================================

        document = self.repository.get_document_by_id(
            db,
            document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        # ======================================================
        # CREATE LOCK
        # ======================================================

        lock = DocumentLock(
            document_id=document_id,
            user_id=user_id,
            locked_at=datetime.utcnow(),
            expires_at=datetime.utcnow()
            + timedelta(minutes=10),
        )

        created_lock = self.lock_repository.create(
            db,
            lock,
        )

        # ======================================================
        # NOTIFY LOCK OWNER
        # ======================================================

        notification_service = NotificationService()

        notification_service.notify_user(
            db=db,
            user_id=user_id,
            title="Document Locked",
            message=(
                f'You have 10 minutes to edit the document '
                f'"{document.title}". Good luck!'
            ),
            notification_type=NotificationType.LOCK,
            level=NotificationLevel.INFO,
            entity_type="document",
            entity_id=document_id,
        )

        return created_lock

    # ==========================================================
    # RELEASE DOCUMENT LOCK
    # ==========================================================

    def release_document_lock(
        self,
        db: Session,
        document_id: int,
    ):
        """
        Release document lock.
        """

        lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        if lock:

            self.lock_repository.delete(
                db,
                lock,
            )

    # ==========================================================
    # LOCK DOCUMENT
    # ==========================================================

    def lock_document(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> DocumentLock:

        return self.create_document_lock(
            db,
            document_id,
            user_id,
        )

    # ==========================================================
    # UNLOCK DOCUMENT
    # ==========================================================

    def unlock_document(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ):
        """
        Release lock only by owner.
        """

        lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        if lock is None:
            return

        if lock.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot release this lock",
            )

        self.lock_repository.delete(
            db,
            lock,
        )
