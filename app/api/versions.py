"""
Version API routes.

This module exposes endpoints
for document section version management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.dependencies.auth_dependency import get_current_user
from app.models.user import User
from app.enums.project_role import ProjectRole
from app.models.project_member import ProjectMember
from app.models.version import Version
from app.models.section import Section
from app.models.document import Document


from app.services.version_service import VersionService

from app.schemas.version_schema import (
    VersionCreate,
    VersionResponse,
    VersionHistoryResponse,
    VersionRestore,
)


router = APIRouter(
    prefix="/versions",
    tags=["Versions"],
)


version_service = VersionService()



@router.post(
    "",
    response_model=VersionResponse,
)
def create_version(
    version_data: VersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new version.
    """

    version = version_service.create_new_version(
        db=db,
        section_id=version_data.section_id,
        author_id=current_user.id,
        title_snapshot=version_data.title_snapshot,
        content_snapshot=version_data.content_snapshot,
        change_comment=version_data.change_comment,
    )

    return version



@router.get(
    "/section/{section_id}",
    response_model=VersionHistoryResponse,
)
def get_section_history(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve section version history.
    """

    versions = version_service.get_history(
        db,
        section_id,
        current_user.id,
    )

    return {
        "versions": versions
    }

@router.get(
    "/archived/{section_id}",
    response_model=VersionHistoryResponse,
)
def get_archived_versions(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve archived versions of a section.
    """

    versions = version_service.get_archived_versions(
        db,
        section_id,
        current_user.id,
    )

    return {
        "versions": versions
    }



@router.get(
    "/current/{section_id}",
    response_model=VersionResponse,
)
def get_current_version(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve current active version.
    """

    version = version_service.get_current_version(
        db,
        section_id,
        current_user.id,
    )


    if version is None:
        raise HTTPException(
            status_code=404,
            detail="No current version found",
        )


    return version



@router.post(
    "/restore",
    response_model=VersionResponse,
)
def restore_version(
    restore_data: VersionRestore,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Restore an old version.
    """

    version = version_service.restore_version(
        db=db,
        version_id=restore_data.version_id,
        author_id=current_user.id,
    )


    if version is None:
        raise HTTPException(
            status_code=404,
            detail="Version not found",
        )


    return version


@router.patch(
    "/{version_id}/archive",
    response_model=VersionResponse,
)
def archive_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Archive a version.

    Only PROJECT_MANAGER can archive versions.
    """


    version = (
        db.query(Version)
        .filter(
            Version.id == version_id
        )
        .first()
    )


    if version is None:
        raise HTTPException(
            status_code=404,
            detail="Version not found",
        )


    # Get document through section
    section = (
        db.query(Section)
        .filter(
            Section.id == version.section_id
        )
        .first()
    )

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )


    document = (
        db.query(Document)
        .filter(
            Document.id == section.document_id
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )


    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
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
            detail="Only PROJECT_MANAGER can archive versions",
        )


    return version_service.archive_version(
    db,
    version_id,
    current_user.id,
)