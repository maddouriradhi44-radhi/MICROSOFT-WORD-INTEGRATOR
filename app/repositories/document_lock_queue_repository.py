"""
Document Lock Queue repository.

This module handles database operations
related to document lock waiting queue.
"""

from sqlalchemy.orm import Session

from app.models.document_lock_queue import DocumentLockQueue
from app.enums.lock_request_status import LockRequestStatus


class DocumentLockQueueRepository:
    """
    Repository responsible for document lock queue operations.
    """


    @staticmethod
    def add_to_queue(
        db: Session,
        queue_item: DocumentLockQueue,
    ) -> DocumentLockQueue:
        """
        Add a user to the document modification queue.
        """

        db.add(queue_item)
        db.commit()
        db.refresh(queue_item)

        return queue_item



    @staticmethod
    def get_queue_by_document(
        db: Session,
        document_id: int,
    ) -> list[DocumentLockQueue]:
        """
        Retrieve waiting users for a document
        using FIFO order.
        """

        return (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.document_id == document_id
            )
            .order_by(
                DocumentLockQueue.requested_at.asc()
            )
            .all()
        )



    @staticmethod
    def get_next_user(
        db: Session,
        document_id: int,
    ) -> DocumentLockQueue | None:
        """
        Retrieve the first waiting user in FIFO order.
        """

        return (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.document_id == document_id,
                DocumentLockQueue.status == LockRequestStatus.WAITING,
            )
            .order_by(
                DocumentLockQueue.requested_at.asc()
            )
            .first()
        )

    @staticmethod
    def remove_from_queue(
        db: Session,
        queue_item: DocumentLockQueue,
    ) -> None:
        """
        Remove a user from the queue
        after getting the lock.
        """

        db.delete(queue_item)
        db.commit()

    @staticmethod
    def get_user_in_queue(
        db: Session,
        document_id: int,
        user_id: int,
    ) -> DocumentLockQueue | None:
        """
        Check whether a user is already waiting
        in the queue.
        """

        return (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.document_id == document_id,
                DocumentLockQueue.user_id == user_id,
            )
            .first()
        )


    @staticmethod
    def get_queue_position(
        db: Session,
        document_id: int,
        user_id: int,
    ) -> int | None:
        """
        Retrieve the user's position in the FIFO queue.
        """

        queue = (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.document_id == document_id
            )
            .order_by(
                DocumentLockQueue.requested_at.asc()
            )
            .all()
        )

        for position, item in enumerate(queue, start=1):
            if item.user_id == user_id:
                return position

        return None


    @staticmethod
    def get_expired_notifications(
        db: Session,
        expiration_time,
    ):
        """
        Retrieve expired notified requests.
        """

        return (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.status
                == LockRequestStatus.NOTIFIED,
                DocumentLockQueue.notified_at <= expiration_time,
            )
            .all()
        )

    @staticmethod
    def get_next_waiting_user(
        db: Session,
        document_id: int,
    ) -> DocumentLockQueue | None:
        """
        Retrieve the first user waiting in FIFO queue.
        Only WAITING requests are considered.
        """

        return (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.document_id == document_id,
                DocumentLockQueue.status == LockRequestStatus.WAITING,
            )
            .order_by(
                DocumentLockQueue.requested_at.asc()
            )
            .first()
        )

    @staticmethod
    def update_status(
        db: Session,
        queue_item: DocumentLockQueue,
        status: LockRequestStatus,
    ) -> DocumentLockQueue:
        """
        Update the status of a lock request.
        """

        queue_item.status = status

        db.commit()
        db.refresh(queue_item)

        return queue_item 
   