"""
Notification API.

This module provides endpoints for managing
notifications of the authenticated user.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User
from app.schemas.notification_schema import (
    NotificationResponse,
    NotificationPaginatedResponse,
)
from app.services.notifications_service import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

notification_service = NotificationService()

@router.get(
    "",
    response_model=NotificationPaginatedResponse,
)
def get_my_notifications(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of notifications per page",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve paginated notifications of the current user.
    """

    return notification_service.get_user_notifications_paginated(
        db,
        current_user.id,
        page,
        page_size,
    )

@router.get(
    "/unread",
    response_model=list[NotificationResponse],
)
def get_my_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all unread notifications of the current user.
    """

    return notification_service.get_unread_notifications(
        db,
        current_user.id,
    )


@router.get(
    "/unread/count",
)
def count_my_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Count unread notifications of the current user.
    """

    count = notification_service.count_unread(
        db,
        current_user.id,
    )

    return {
        "count": count,
    }


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a specific notification.
    """

    notification = notification_service.get_notification(
        db,
        notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this notification.",
        )

    return notification


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a notification as read.
    """

    notification = notification_service.get_notification(
        db,
        notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this notification.",
        )

    return notification_service.mark_as_read(
        db,
        notification_id,
    )


@router.patch(
    "/read-all",
)
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark all notifications of the current user as read.
    """

    count = notification_service.mark_all_as_read(
        db,
        current_user.id,
    )

    return {
        "message": "All notifications marked as read.",
        "count": count,
    }


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a notification belonging to the current user.
    """

    notification = notification_service.get_notification(
        db,
        notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this notification.",
        )

    notification_service.delete_notification(
        db,
        notification_id,
    )

    return None