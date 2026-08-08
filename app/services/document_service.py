from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_lock import DocumentLock

from app.repositories.document_repository import DocumentRepository
from app.repositories.document_lock_repository import DocumentLockRepository

from app.schemas.document_schema import (
    DocumentCreate,
    DocumentUpdate,
)

from app.services.permission_service import PermissionService
from app.services.storage_service import StorageService


from app.services.docx_analyzer_service import (
    DocxAnalyzerService
)

from app.services.section_service import SectionService

class DocumentService:
    """
    Business logic related to documents.
    """

    def __init__(self):
        self.repository = DocumentRepository()
        self.lock_repository = DocumentLockRepository()


    def create_document(
        self,
        db: Session,
        document_data: DocumentCreate,
        owner_id: int,
        storage_key: str,
        original_filename: str,
        )-> Document:
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


        storage_service = StorageService()

        absolute_path = storage_service.get_absolute_path(
            created_document.storage_key
        )


        analyzer = DocxAnalyzerService()

        sections = analyzer.analyze(
            absolute_path
        )


        section_service = SectionService()

        section_service.create_sections(
            db,
            created_document.id,
            created_document.project_id,
            sections,
        )


        return created_document    


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



    def prepare_docx_import(
        self,
        file_path: str,
    ) -> None:
        """
        Placeholder for future DOCX import.
        """

        pass



    def get_document_by_id(
        self,
        db: Session,
        document_id: int,
    ) -> Document | None:

        return self.repository.get_document_by_id(
            db,
            document_id,
        )



    def get_project_documents(
        self,
        db: Session,
        project_id: int,
    ) -> list[Document]:

        return self.repository.get_project_documents(
            db,
            project_id,
        )



    def update_document(
        self,
        db: Session,
        document_id: int,
        document_data: DocumentUpdate,
        user_id: int,
    ) -> Document | None:
        """
        Update document safely using lock system.
        """


        document = self.repository.get_document_by_id(
            db,
            document_id,
        )


        if document is None:
            return None



        PermissionService.check_project_manager(
            db,
            document.project_id,
            user_id,
        )



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



        updates = document_data.model_dump(
            exclude_unset=True
        )


        temporary_lock = False


        # No existing lock -> create temporary lock
        if existing_lock is None:

            self.create_document_lock(
                db,
                document_id,
                user_id,
            )

            temporary_lock = True



        try:

            updated_document = self.repository.update_document(
                db,
                document,
                updates,
            )


        finally:

            if temporary_lock:

                self.release_document_lock(
                    db,
                    document_id,
                )


        return updated_document




    def delete_document(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> bool:


        document = self.repository.get_document_by_id(
            db,
            document_id,
        )


        if document is None:
            return False



        PermissionService.check_project_manager(
            db,
            document.project_id,
            user_id,
        )


        self.repository.delete_document(
            db,
            document,
        )


        return True




    def create_document_lock(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ) -> DocumentLock:
        """
        Create document lock.
        """


        existing_lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )


        if existing_lock:

            raise HTTPException(
                status_code=423,
                detail="Document is currently locked",
            )



        lock = DocumentLock(
            document_id=document_id,
            user_id=user_id,
            locked_at=datetime.utcnow(),
            expires_at=datetime.utcnow()
            + timedelta(minutes=10),
        )



        return self.lock_repository.create(
            db,
            lock,
        )




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