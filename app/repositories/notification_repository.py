"""
Notification repository.

This module handles database operations related
to notifications.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:
    """
    Repository responsible for notification database operations.
    """

    def create(
        self,
        db: Session,
        notification: Notification,
    ) -> Notification:
        """
        Create a notification.
        """

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    def get_by_id(
        self,
        db: Session,
        notification_id: int,
    ) -> Notification | None:
        """
        Retrieve a notification by its ID.
        """

        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Notification]:
        """
        Retrieve all notifications belonging to a user.
        """

        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )


    def mark_as_read(
        self,
        db: Session,
        notification: Notification,
    ) -> Notification:
        """
        Mark a notification as read.
        """

        notification.is_read = True
        notification.read_at = datetime.utcnow()

        db.commit()
        db.refresh(notification)

        return notification

    def mark_all_as_read(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        """
        Mark all unread notifications of a user as read.

        Returns the number of notifications updated.
        """

        notifications = (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .all()
        )

        read_at = datetime.utcnow()

        for notification in notifications:
            notification.is_read = True
            notification.read_at = read_at

        db.commit()

        return len(notifications)

    def delete(
        self,
        db: Session,
        notification: Notification,
    ) -> None:
        """
        Delete a notification.
        """

        db.delete(notification)
        db.commit()


    def get_unread(
        self,
        db: Session,
        user_id: int,
    ) -> list[Notification]:
        """
        Retrieve all unread notifications of a user.
        """

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .order_by(Notification.created_at.desc())
            .all()
        )


    def count_unread(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        """
        Count unread notifications of a user.
        """

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .count()
        )
