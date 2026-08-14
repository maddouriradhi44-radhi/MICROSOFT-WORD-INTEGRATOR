"""
Validation API routes.

This module exposes endpoints
for section version validation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth_dependency import get_current_user

from app.models.user import User
from app.models.validation import Validation
from app.models.version import Version

from app.enums.project_role import ProjectRole
from app.models.project_member import ProjectMember

from app.schemas.validation import (
    ValidationCreate,
    ValidationDecision,
    ValidationResponse,
)

from app.services.validation_service import ValidationService


router = APIRouter(
    prefix="/validations",
    tags=["Validations"],
)


validation_service = ValidationService()


@router.post(
    "",
    response_model=ValidationResponse,
)
def create_validation(
    validation_data: ValidationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit a version for validation.
    """

    try:
        return validation_service.create_validation(
            db=db,
            version_id=validation_data.version_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.get(
    "/version/{version_id}",
    response_model=ValidationResponse,
)
def get_validation_by_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve validation associated with a version.
    """

    validation = validation_service.get_validation_by_version(
        db,
        version_id,
    )

    if validation is None:
        raise HTTPException(
            status_code=404,
            detail="Validation not found",
        )

    return validation


@router.get(
    "/section/{section_id}",
    response_model=list[ValidationResponse],
)
def get_validation_history(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve validation history for a section.
    """

    return validation_service.get_validation_history(
        db,
        section_id,
    )


@router.patch(
    "/{validation_id}/approve",
    response_model=ValidationResponse,
)
def approve_validation(
    validation_id: int,
    decision: ValidationDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Approve a validation.

    Only PROJECT_MANAGER can approve validations.
    """

    validation = (
        db.query(Validation)
        .filter(
            Validation.id == validation_id
        )
        .first()
    )

    if validation is None:
        raise HTTPException(
            status_code=404,
            detail="Validation not found",
        )

    version = (
        db.query(Version)
        .filter(
            Version.id == validation.version_id
        )
        .first()
    )

    if version is None:
        raise HTTPException(
            status_code=404,
            detail="Version not found",
        )

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == version.section.project_id,
            ProjectMember.user_id == current_user.id,
        )
        .first()
    )

    if (
        member is None
        or member.role != ProjectRole.PROJECT_MANAGER
    ):
        raise HTTPException(
            status_code=403,
            detail="Only PROJECT_MANAGER can approve validations",
        )

    try:
        return validation_service.approve_validation(
            db=db,
            validation_id=validation_id,
            reviewer_id=current_user.id,
            comment=decision.comment,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.patch(
    "/{validation_id}/reject",
    response_model=ValidationResponse,
)
def reject_validation(
    validation_id: int,
    decision: ValidationDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Reject a validation.

    Only PROJECT_MANAGER can reject validations.
    """

    validation = (
        db.query(Validation)
        .filter(
            Validation.id == validation_id
        )
        .first()
    )

    if validation is None:
        raise HTTPException(
            status_code=404,
            detail="Validation not found",
        )

    version = (
        db.query(Version)
        .filter(
            Version.id == validation.version_id
        )
        .first()
    )

    if version is None:
        raise HTTPException(
            status_code=404,
            detail="Version not found",
        )

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == version.section.project_id,
            ProjectMember.user_id == current_user.id,
        )
        .first()
    )

    if (
        member is None
        or member.role != ProjectRole.PROJECT_MANAGER
    ):
        raise HTTPException(
            status_code=403,
            detail="Only PROJECT_MANAGER can reject validations",
        )

    if not decision.comment:
        raise HTTPException(
            status_code=400,
            detail="A comment is required when rejecting a validation",
        )

    try:
        return validation_service.reject_validation(
            db=db,
            validation_id=validation_id,
            reviewer_id=current_user.id,
            comment=decision.comment,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )