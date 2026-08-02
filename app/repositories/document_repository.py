from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    """
    Database operations related to documents.
    """

    def create_document(
        self,
        db: Session,
        document: Document,
    ) -> Document:
        """
        Save a new document to the database.
        """

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def get_document_by_id(
        self,
        db: Session,
        document_id: int,
    ) -> Document | None:
        """
        Retrieve a document by its ID.
        """

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def get_project_documents(
        self,
        db: Session,
        project_id: int,
    ) -> list[Document]:
        """
        Retrieve all documents belonging to a project.
        """

        return (
            db.query(Document)
            .filter(Document.project_id == project_id)
            .all()
        )

    def update_document(
        self,
        db: Session,
        document: Document,
        updates: dict,
    ) -> Document:
        """
        Update an existing document.
        """

        for field, value in updates.items():
            setattr(document, field, value)

        db.commit()
        db.refresh(document)

        return document

    def delete_document(
        self,
        db: Session,
        document: Document,
    ) -> bool:
        """
        Delete a document from the database.
        """

        db.delete(document)
        db.commit()

        return True