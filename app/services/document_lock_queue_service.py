from datetime import datetime , timedelta,timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums.lock_request_status import LockRequestStatus

from app.models.document_lock_queue import DocumentLockQueue

from app.repositories.document_lock_repository import (
    DocumentLockRepository,
)
from app.repositories.document_lock_queue_repository import (
    DocumentLockQueueRepository,
)

from app.services.document_service import DocumentService

from app.services.notifications_service import NotificationService

from app.enums.notification_level import NotificationLevel
from app.enums.notification_type import NotificationType


class DocumentLockQueueService:
    """
    Business logic related to the document lock queue.
    """

    def __init__(self):
        self.lock_repository = DocumentLockRepository()
        self.queue_repository = DocumentLockQueueRepository()
        self.document_service = DocumentService()
        self.notification_service = NotificationService()

    def request_lock(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ):
        """
        Request permission to modify a document.
        """

        existing_lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        # User already owns the lock
        if (
            existing_lock
            and existing_lock.user_id == user_id
        ):
            raise HTTPException(
                status_code=409,
                detail="You already own the document lock.",
            )

        # Document is free -> lock immediately
        if existing_lock is None:
            return self.document_service.create_document_lock(
                db,
                document_id,
                user_id,
            )

        # User already waiting
        existing_queue = (
            self.queue_repository.get_user_in_queue(
                db,
                document_id,
                user_id,
            )
        )

        if existing_queue:
            raise HTTPException(
                status_code=409,
                detail="User is already in the queue.",
            )

        queue_item = DocumentLockQueue(
            document_id=document_id,
            user_id=user_id,
            requested_at=datetime.now(timezone.utc),
            status=LockRequestStatus.WAITING,
        )

        queue_item = self.queue_repository.add_to_queue(
            db,
            queue_item,
        )

        # ======================================================
        # NOTIFY THE USER WHO REQUESTED THE LOCK
        # ======================================================

        now = datetime.utcnow()

        remaining_seconds = max(
            0,
            int(
                (
                    existing_lock.expires_at - now
                ).total_seconds()
            ),
        )

        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        time_remaining = f"{minutes:02d}:{seconds:02d}"

        self.notification_service.notify_user(
            db=db,
            user_id=user_id,
            title="Document Currently Locked",
            message=(
                "Another user is currently editing this document.\n"
                f"Time remaining: {time_remaining}"
            ),
            notification_type=NotificationType.LOCK,
            level=NotificationLevel.INFO,
            entity_type="document",
            entity_id=document_id,
        )

        return queue_item

    def release_lock(
        self,
        db: Session,
        document_id: int,
    ):
        """
        Release the current lock and notify
        the first waiting user.
        """

        # ======================================================
        # REMOVE CURRENT LOCK
        # ======================================================

        self.document_service.release_document_lock(
            db,
            document_id,
        )

        # ======================================================
        # GET FIRST WAITING USER (FIFO)
        # ======================================================

        next_user = (
            self.queue_repository.get_next_waiting_user(
                db,
                document_id,
            )
        )

        if next_user is None:
            return {
                "message": "No user waiting."
            }

        # ======================================================
        # MARK USER AS NOTIFIED
        # ======================================================

        next_user.notified_at = datetime.now(timezone.utc)

        self.queue_repository.update_status(
            db,
            next_user,
            LockRequestStatus.NOTIFIED,
        )

        # ======================================================
        # SEND NOTIFICATION TO NEXT USER ONLY
        # ======================================================

        self.notification_service.notify_user(
            db=db,
            user_id=next_user.user_id,
            title="Document Available",
            message=(
                "The document is now available for editing.\n"
                "Do you want to edit it?\n"
                "Time remaining: 01:00"
            ),
            notification_type=NotificationType.LOCK,
            level=NotificationLevel.INFO,
            entity_type="document",
            entity_id=document_id,
        )

        return {
            "message": "Next user has been notified.",
            "document_id": document_id,
            "user_id": next_user.user_id,
        }

    def get_queue_status(
        self,
        db: Session,
        document_id: int,
    ) -> dict:
        """
        Retrieve queue information.
        """

        current_lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        queue = (
            self.queue_repository.get_queue_by_document(
                db,
                document_id,
            )
        )

        return {
            "locked": current_lock is not None,
            "current_lock": current_lock,
            "queue": queue,
            "waiting_users": len(queue),
        }

    def accept_lock(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ):
        """
        User accepts the modification request
        after being notified.
        """

        request = self.queue_repository.get_user_in_queue(
            db,
            document_id,
            user_id,
        )

        if request is None:
            raise HTTPException(
                status_code=404,
                detail="No lock request found.",
            )

        if request.status != LockRequestStatus.NOTIFIED:
            raise HTTPException(
                status_code=400,
                detail="Request is not ready.",
            )

        # Verify that document is free
        existing_lock = self.lock_repository.get_by_document(
            db,
            document_id,
        )

        if existing_lock:
            raise HTTPException(
                status_code=423,
                detail="Document is already locked.",
            )

        # Give lock to the user
        lock = self.document_service.create_document_lock(
            db,
            document_id,
            user_id,
        )

        # Update request status
        self.queue_repository.update_status(
            db,
            request,
            LockRequestStatus.ACCEPTED,
        )

        # Remove from queue
        self.queue_repository.remove_from_queue(
            db,
            request,
        )

        return {
            "message": "Lock accepted.",
            "document_id": document_id,
            "user_id": user_id,
            "lock": lock,
        }


    def refuse_lock(
        self,
        db: Session,
        document_id: int,
        user_id: int,
    ):
        """
        User refuses the modification request.
        """

        request = self.queue_repository.get_user_in_queue(
            db,
            document_id,
            user_id,
        )

        if request is None:
            raise HTTPException(
                status_code=404,
                detail="Request not found.",
            )

        if request.status != LockRequestStatus.NOTIFIED:
            raise HTTPException(
                status_code=400,
                detail="Request is not ready.",
            )

        # ======================================================
        # UPDATE REQUEST STATUS
        # ======================================================

        self.queue_repository.update_status(
            db,
            request,
            LockRequestStatus.REFUSED,
        )

        # ======================================================
        # NOTIFY THE USER WHO REFUSED
        # ======================================================

        self.notification_service.notify_user(
            db=db,
            user_id=user_id,
            title="Document Edit Request Refused",
            message=(
                "You cannot edit this document at this time."
            ),
            notification_type=NotificationType.LOCK,
            level=NotificationLevel.INFO,
            entity_type="document",
            entity_id=document_id,
        )

        # ======================================================
        # REMOVE USER FROM QUEUE
        # ======================================================

        self.queue_repository.remove_from_queue(
            db,
            request,
        )

        # ======================================================
        # NOTIFY NEXT USER IN FIFO
        # ======================================================

        return self.release_lock(
            db,
            document_id,
        )


    def expire_old_requests(
        self,
        db: Session,
    ):
        """
        Expire notified requests after 1 minute
        without user response.
        """

        expiration_time = (
            datetime.now(timezone.utc) - timedelta(minutes=1)
        )

        print("===== SCHEDULER CHECK =====")
        print("NOW UTC:", datetime.now(timezone.utc))
        print("EXPIRATION TIME:", expiration_time)


        expired_requests = (
            db.query(DocumentLockQueue)
            .filter(
                DocumentLockQueue.status
                == LockRequestStatus.NOTIFIED,
                DocumentLockQueue.notified_at <= expiration_time,
            )
            .all()
        )


        print("EXPIRED FOUND:", len(expired_requests))


        for request in expired_requests:

            print(
                "EXPIRING REQUEST:",
                request.id,
                "USER:",
                request.user_id,
                "NOTIFIED AT:",
                request.notified_at
            )

            self.queue_repository.update_status(
                db,
                request,
                LockRequestStatus.EXPIRED,
            )

            self.queue_repository.remove_from_queue(
                db,
                request,
            )

            self.release_lock(
                db,
                request.document_id,
            )


        return {
            "expired_requests": len(expired_requests)
        }