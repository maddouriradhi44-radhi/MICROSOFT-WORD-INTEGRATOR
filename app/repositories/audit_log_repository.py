"""
Audit log repository.

This module handles database operations related
to audit logs.
"""

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogRepository:
    """
    Repository responsible for audit log database operations.
    """

    def create(
        self,
        db: Session,
        audit_log: AuditLog,
    ) -> AuditLog:
        """
        Create an audit log entry.
        """

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)

        return audit_log

    def get_by_id(
        self,
        db: Session,
        audit_log_id: int,
    ) -> AuditLog | None:
        """
        Retrieve an audit log by its ID.
        """

        return (
            db.query(AuditLog)
            .filter(AuditLog.id == audit_log_id)
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:
        """
        Retrieve all audit logs created by a user.
        """

        return (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
            .all()
        )

    def get_all(
        self,
        db: Session,
    ) -> list[AuditLog]:
        """
        Retrieve all audit logs.
        """

        return (
            db.query(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .all()
        )

    def get_by_action(
        self,
        db: Session,
        action: str,
    ) -> list[AuditLog]:
        """
        Retrieve audit logs filtered by action.
        """

        return (
            db.query(AuditLog)
            .filter(AuditLog.action == action)
            .order_by(AuditLog.created_at.desc())
            .all()
        )