"""
Notification service.

This module contains the business logic related
to notifications.
"""


from sqlalchemy.orm import Session

from app.enums.notification_level import NotificationLevel
from app.enums.notification_type import NotificationType
from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    """
    Service responsible for notification business logic.
    """

    def __init__(self) -> None:
        self.repository = NotificationRepository()

    def create_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        level: NotificationLevel = NotificationLevel.INFO,
        entity_type: str | None = None,
        entity_id: int | None = None,
    ) -> Notification:
        """
        Create a notification for a user.
        """

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            level=level,
            entity_type=entity_type,
            entity_id=entity_id,
        )

        return self.repository.create(
            db,
            notification,
        )

    def notify_user(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        level: NotificationLevel = NotificationLevel.INFO,
        entity_type: str | None = None,
        entity_id: int | None = None,
    ) -> Notification:
        """
        Notify a specific user.

        This method is the main entry point that other
        modules should use to send a notification.
        """

        return self.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            level=level,
            entity_type=entity_type,
            entity_id=entity_id,
        )

    def get_notification(
        self,
        db: Session,
        notification_id: int,
    ) -> Notification | None:
        """
        Retrieve a notification by its ID.
        """

        return self.repository.get_by_id(
            db,
            notification_id,
        )

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
    ) -> list[Notification]:
        """
        Retrieve all notifications of a user.
        """

        return self.repository.get_by_user(
            db,
            user_id,
        )

    def get_unread_notifications(
        self,
        db: Session,
        user_id: int,
    ) -> list[Notification]:
        """
        Retrieve all unread notifications of a user.
        """

        return self.repository.get_unread(
            db,
            user_id,
        )

    def count_unread(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        """
        Count unread notifications of a user.
        """

        return self.repository.count_unread(
            db,
            user_id,
        )

    def mark_as_read(
        self,
        db: Session,
        notification_id: int,
    ) -> Notification | None:
        """
        Mark a notification as read.
        """

        notification = self.repository.get_by_id(
            db,
            notification_id,
        )

        if notification is None:
            return None

        return self.repository.mark_as_read(
            db,
            notification,
        )

    def mark_all_as_read(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        """
        Mark all unread notifications of a user as read.
        """

        return self.repository.mark_all_as_read(
            db,
            user_id,
        )

    def delete_notification(
        self,
        db: Session,
        notification_id: int,
    ) -> bool:
        """
        Delete a notification.
        """

        notification = self.repository.get_by_id(
            db,
            notification_id,
        )

        if notification is None:
            return False

        self.repository.delete(
            db,
            notification,
        )

        return True