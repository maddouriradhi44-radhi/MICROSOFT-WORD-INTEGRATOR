from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.document_service import DocumentService
from app.schemas.document_schema import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()

@router.post(
    "/",
    response_model=DocumentResponse,
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
):
    return document_service.create_document(
        db,
        document,
        owner_id=1,
    )

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)

def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = document_service.get_document_by_id(
        db,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return document

@router.get(
    "/project/{project_id}",
    response_model=list[DocumentResponse],
)
def get_project_documents(
    project_id: int,
    db: Session = Depends(get_db),
):
    return document_service.get_project_documents(
        db,
        project_id,
    )

@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
)
def update_document(
    document_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db),
):
    updated_document = document_service.update_document(
        db,
        document_id,
        document,
    )

    if updated_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return updated_document

@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    deleted = document_service.delete_document(
        db,
        document_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "message": "Document deleted successfully"
    }