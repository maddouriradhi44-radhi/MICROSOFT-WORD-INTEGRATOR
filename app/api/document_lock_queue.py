from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth_dependency import get_current_user

from app.models.user import User

from app.services.document_lock_queue_service import (
    DocumentLockQueueService,
)

router = APIRouter(
    prefix="/document-lock-queue",
    tags=["Document Lock Queue"],
)

queue_service = DocumentLockQueueService()

@router.post(
    "/{document_id}/request-lock",
)
def request_lock(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return queue_service.request_lock(
        db,
        document_id,
        current_user.id,
    )

@router.post(
    "/{document_id}/release-lock",
)
def release_lock(
    document_id: int,
    db: Session = Depends(get_db),
):
    return queue_service.release_lock(
        db,
        document_id,
    )


@router.get(
    "/{document_id}/status",
)
def get_queue_status(
    document_id: int,
    db: Session = Depends(get_db),
):
    return queue_service.get_queue_status(
        db,
        document_id,
    )

@router.post(
    "/{document_id}/accept-lock",
)
def accept_lock(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Accept modification permission.
    """

    return queue_service.accept_lock(
        db,
        document_id,
        current_user.id,
    )


@router.post(
    "/{document_id}/refuse-lock",
)
def refuse_lock(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Refuse modification permission.
    """

    return queue_service.refuse_lock(
        db,
        document_id,
        current_user.id,
    )

