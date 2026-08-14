from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth_dependency import get_current_user

from app.models.user import User
from app.services.document_service import DocumentService
from app.schemas.document_schema import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
)
from app.services.storage_service import StorageService
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User


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
    title: str = Form(...),
    project_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    storage_service = StorageService()

    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are allowed",
        )

    storage_key = storage_service.save_file(
        file
    )


    document_data = DocumentCreate(
        title=title,
        project_id=project_id,
    )


    return document_service.create_document(
        db=db,
        document_data=document_data,
        owner_id=current_user.id,
        storage_key=storage_key,
        original_filename=file.filename,
    )

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    updated_document = document_service.update_document(
        db,
        document_id,
        document,
        current_user.id,
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
    current_user: User = Depends(get_current_user),
):
    deleted = document_service.delete_document(
        db,
        document_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "message": "Document deleted successfully"
    }

@router.post("/{document_id}/lock")
def lock_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lock = document_service.lock_document(
        db,
        document_id,
        current_user.id,
    )

    return {
        "message": "Document locked successfully",
        "expires_at": lock.expires_at,
    }


@router.delete("/{document_id}/lock")
def unlock_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document_service.unlock_document(
        db,
        document_id,
        current_user.id,
    )

    return {
        "message": "Document unlocked successfully"
    }