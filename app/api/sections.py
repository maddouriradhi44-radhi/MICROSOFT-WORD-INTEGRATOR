"""
Section API.

This module exposes endpoints
for managing document sections.
"""
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from pathlib import Path

from app.services.export_service import ExportService

from app.database.session import get_db

from app.dependencies.auth_dependency import get_current_user

from app.models.user import User

from app.services.section_service import SectionService

from app.schemas.section_schema import (
    SectionCreate,
    SectionUpdate,
    SectionResponse,
)
from app.services.import_service import ImportService

router = APIRouter(
    prefix="/sections",
    tags=["Sections"],
)


section_service = SectionService()
export_service = ExportService()
import_service = ImportService()
# ==========================================================
# Create section
# ==========================================================

@router.post(
    "/",
    response_model=SectionResponse,
)
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return section_service.create_section(
        db=db,
        section_data=section,
        user_id=current_user.id,
    )


@router.get(
    "/my-sections",
    response_model=list[SectionResponse],
)
def get_my_sections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get sections assigned to current user.
    """

    return section_service.get_user_sections(
        db,
        current_user.id,
    )

@router.get(
    "/project/{project_id}",
    response_model=list[SectionResponse],
)
def get_project_sections(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all sections belonging to a project.
    """

    return section_service.get_project_sections(
        db,
        project_id,
    )

# ==========================================================
# Export section
# ==========================================================

@router.get(
    "/{section_id}/export",
)
def export_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Export a single section as a DOCX file.
    """

    output_path = (
        Path("storage")
        / "exports"
        / f"section_{section_id}_export.docx"
    )

    result = export_service.export_section(
        db=db,
        section_id=section_id,
        user_id=current_user.id,
        output_path=output_path,
    )

    return FileResponse(
        path=result,
        media_type=(
            "application/vnd.openxmlformats-officedocument"
            ".wordprocessingml.document"
        ),
        filename=f"section_{section_id}.docx",
    )

# ==========================================================
# IMPORT  section
# ==========================================================


@router.post(
    "/{section_id}/import",
)
def import_section(
    section_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Import an externally edited DOCX section.

    The file is parsed and compared with the current section.
    No new version is created at this stage.
    """

    if file.content_type != (
        "application/vnd.openxmlformats-officedocument"
        ".wordprocessingml.document"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are allowed",
        )

    try:
        result = import_service.import_section(
            db=db,
            section_id=section_id,
            user_id=current_user.id,
            file=file,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )

    return result


# ==========================================================
# Get section by id
# ==========================================================

@router.get(
    "/{section_id}",
    response_model=SectionResponse,
)
def get_section(
    section_id: int,
    db: Session = Depends(get_db),
):

    section = section_service.get_section_by_id(
        db,
        section_id,
    )


    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )


    return section



# ==========================================================
# Get document sections
# ==========================================================

@router.get(
    "/document/{document_id}",
    response_model=list[SectionResponse],
)
def get_document_sections(
    document_id: int,
    db: Session = Depends(get_db),
):

    return section_service.get_document_sections(
        db,
        document_id,
    )



# ==========================================================
# Get user assigned sections
# ==========================================================

@router.get(
    "/user/{user_id}",
    response_model=list[SectionResponse],
)
def get_user_sections(
    user_id: int,
    db: Session = Depends(get_db),
):

    return section_service.get_user_sections(
        db,
        user_id,
    )



# ==========================================================
# Update section
# ==========================================================

@router.patch(
    "/{section_id}",
    response_model=SectionResponse,
)
def update_section(
    section_id: int,
    section: SectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    updated_section = section_service.update_section(
        db,
        section_id,
        section,
        current_user.id,
    )


    if updated_section is None:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )


    return updated_section


@router.put(
    "/{section_id}/assign/{user_id}",
    response_model=SectionResponse,
)
def assign_section(
    section_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Assign a section to a project member.

    Only PROJECT_MANAGER can assign sections.
    """

    section = section_service.assign_section(
        db=db,
        section_id=section_id,
        assigned_user_id=user_id,
        current_user_id=current_user.id,
    )

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Section or user not found",
        )

    return section


# ==========================================================
# Delete section
# ==========================================================

@router.delete(
    "/{section_id}",
)
def delete_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    deleted = section_service.delete_section(
        db,
        section_id,
        current_user.id,
    )


    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )


    return {
        "message": "Section deleted successfully"
    }
