"""
Notification schemas.

This module defines Pydantic schemas used
for notification API responses.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.notification_level import NotificationLevel
from app.enums.notification_type import NotificationType


class NotificationResponse(BaseModel):
    """
    Schema returned when retrieving a notification.
    """

    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    level: NotificationLevel
    is_read: bool
    read_at: datetime | None
    entity_type: str | None
    entity_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)