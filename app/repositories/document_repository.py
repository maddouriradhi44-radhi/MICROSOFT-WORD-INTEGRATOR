from sqlalchemy.orm import Session
from app.models.document import Document


class DocumentRepository:
    """Database operations related to documents."""


    def create_document(self, db: Session, document: Document) -> Document:

        db.add(document)
        db.commit()
        db.refresh(document)
        return document
        """Save a new document to the database."""



    def get_document_by_id(
        self,
        db: Session,
        document_id: int,
    ) -> Document | None:

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )
        """Retrieve a document by its ID."""


    def get_project_documents(
        self,
        db: Session,
        project_id: int,
    ) -> list[Document]:

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

        for field, value in updates.items():
            setattr(document, field, value)

        db.commit()
        db.refresh(document)

        return document

    def delete_document(
        self,
        db: Session,
        document: Document,
    ) -> None:

        db.delete(document)
        db.commit()