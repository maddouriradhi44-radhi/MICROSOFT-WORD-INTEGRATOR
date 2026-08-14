"""
Audit log service.

This module contains the business logic
for audit log operations.
"""

from sqlalchemy.orm import Session

from app.enums.audit_action import AuditAction
from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:
    """
    Service responsible for audit log operations.
    """

    def __init__(self):
        self.repository = AuditLogRepository()

    def log_action(
        self,
        db: Session,
        user_id: int,
        action: AuditAction,
        target: str,
    ) -> AuditLog:
        """
        Record an action performed by a user.
        """

        audit_log = AuditLog(
            user_id=user_id,
            action=action.value,
            target=target,
        )

        return self.repository.create(
            db=db,
            audit_log=audit_log,
        )

    def get_all(
        self,
        db: Session,
    ) -> list[AuditLog]:
        """
        Retrieve all audit logs.
        """

        return self.repository.get_all(db)

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:
        """
        Retrieve audit logs created by a specific user.
        """

        return self.repository.get_by_user(
            db,
            user_id,
        )

    def get_by_action(
        self,
        db: Session,
        action: str,
    ) -> list[AuditLog]:
        """
        Retrieve audit logs filtered by action.
        """

        return self.repository.get_by_action(
            db,
            action,
        )