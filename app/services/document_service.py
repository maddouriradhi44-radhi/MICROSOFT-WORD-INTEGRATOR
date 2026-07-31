from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_schema import (
    DocumentCreate,
    DocumentUpdate,
)

class DocumentService:
    """Business logic related to documents."""

    def __init__(self):
        self.repository = DocumentRepository()



    """Create and persist a new document."""

    def create_document(
        self,
        db: Session,
        document_data: DocumentCreate,
        owner_id: int,
    ) -> Document:


        document = Document(
            title=document_data.title,
            file_path=document_data.file_path,
            owner_id=owner_id,
            project_id=document_data.project_id,
        )

        return self.repository.create_document(db, document)



    """Associate an existing document with a project."""

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
            {"project_id": project_id},
        )

    def verify_project_owner(
        self,
        project_id: int,
        user_id: int,
    ) -> bool:
        """
        Verify that the given user owns the project.

        Future implementation:
        - Retrieve the project from the database.
        - Compare project.owner_id with user_id.
        - Raise an exception if the user is not the owner.
        """

        # Placeholder until ProjectRepository is implemented.
        return True

    def prepare_docx_import(
        self,
        file_path: str,
    ) -> None:
        """
        Placeholder for future DOCX import.

        Future responsibilities:
        - Validate the .docx file.
        - Extract the document content.
        - Split the document into sections.
        - Store extracted data in the database.
        """
        pass

def get_document_by_id(
    self,
    db: Session,
    document_id: int,
) -> Document | None:
    """Retrieve a document by ID."""

    return self.repository.get_document_by_id(
        db,
        document_id,
    )

def get_project_documents(
    self,
    db: Session,
    project_id: int,
) -> list[Document]:
    """Retrieve all documents of a project."""

    return self.repository.get_project_documents(
        db,
        project_id,
    )

def update_document(
    self,
    db: Session,
    document_id: int,
    document_data: DocumentUpdate,
) -> Document | None:
    """Update an existing document."""

    document = self.repository.get_document_by_id(
        db,
        document_id,
    )

    if document is None:
        return None

    updates = document_data.model_dump(
        exclude_unset=True
    )

    return self.repository.update_document(
        db,
        document,
        updates,
    )

def delete_document(
    self,
    db: Session,
    document_id: int,
) -> bool:
    """Delete an existing document."""

    document = self.repository.get_document_by_id(
        db,
        document_id,
    )

    if document is None:
        return False

    self.repository.delete_document(
        db,
        document,
    )

    return True