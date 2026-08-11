"""
Document Lock repository.

This module handles database operations
related to document locks.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.document_lock import DocumentLock


class DocumentLockRepository:
    """
    Repository responsible for DocumentLock operations.
    """

    @staticmethod
    def get_by_document(
        db: Session,
        document_id: int,
    ) -> DocumentLock | None:
        """
        Retrieve the active lock of a document.

        If the lock has expired, it is automatically deleted
        and None is returned.
        """

        lock = (
            db.query(DocumentLock)
            .filter(
                DocumentLock.document_id == document_id
            )
            .first()
        )

        if lock is None:
            return None

        # Check expiration
        if lock.expires_at <= datetime.utcnow():

            db.delete(lock)
            db.commit()

            return None

        return lock

    @staticmethod
    def create(
        db: Session,
        lock: DocumentLock,
    ) -> DocumentLock:
        """
        Create a new document lock.
        """

        db.add(lock)
        db.commit()
        db.refresh(lock)

        return lock

    @staticmethod
    def delete(
        db: Session,
        lock: DocumentLock,
    ) -> None:
        """
        Delete an existing document lock.
        """

        db.delete(lock)
        db.commit()