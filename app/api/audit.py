"""
Audit API.

This module exposes endpoints for audit log consultation.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.role_dependency import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.audit_log_schema import AuditLogResponse
from app.services.audit_log_service import AuditLogService

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
)
audit_log_service = AuditLogService()


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.PROJECT_MANAGER)
    ),
):
    """
    Retrieve audit logs.

    Only PROJECT_MANAGER users can access audit logs.
    """

    return audit_log_service.get_all(db)


@router.get(
    "/user/{user_id}",
    response_model=list[AuditLogResponse],
)
def get_audit_logs_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.PROJECT_MANAGER)
    ),
):
    """
    Retrieve audit logs created by a specific user.
    """

    return audit_log_service.get_by_user(
        db,
        user_id,
    )


@router.get(
    "/action/{action}",
    response_model=list[AuditLogResponse],
)
def get_audit_logs_by_action(
    action: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.PROJECT_MANAGER)
    ),
):
    """
    Retrieve audit logs filtered by action.
    """

    return audit_log_service.get_by_action(
        db,
        action,
    )

