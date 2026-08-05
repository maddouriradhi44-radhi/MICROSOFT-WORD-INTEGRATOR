"""
Document block API.

This module exposes endpoints
for managing document blocks.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.database.session import get_db

from app.services.document_block_service import (
    DocumentBlockService,
)

from app.schemas.document_block_schema import (
    DocumentBlockCreate,
    DocumentBlockUpdate,
    DocumentBlockResponse,
)



router = APIRouter(
    prefix="/document-blocks",
    tags=["Document Blocks"],
)



document_block_service = DocumentBlockService()



# ==========================================================
# Create block
# ==========================================================

@router.post(
    "/",
    response_model=DocumentBlockResponse,
)
def create_block(
    block: DocumentBlockCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new document block.
    """

    return document_block_service.create_block(
        db,
        block,
    )



# ==========================================================
# Get block by id
# ==========================================================

@router.get(
    "/{block_id}",
    response_model=DocumentBlockResponse,
)
def get_block(
    block_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a document block by id.
    """


    block = document_block_service.get_block_by_id(
        db,
        block_id,
    )


    if block is None:
        raise HTTPException(
            status_code=404,
            detail="Document block not found",
        )


    return block



# ==========================================================
# Get section blocks
# ==========================================================

@router.get(
    "/section/{section_id}",
    response_model=list[DocumentBlockResponse],
)
def get_section_blocks(
    section_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve all blocks belonging to a section.
    """


    return document_block_service.get_section_blocks(
        db,
        section_id,
    )



# ==========================================================
# Update block
# ==========================================================

@router.patch(
    "/{block_id}",
    response_model=DocumentBlockResponse,
)
def update_block(
    block_id: int,
    block: DocumentBlockUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing document block.
    """


    updated_block = document_block_service.update_block(
        db,
        block_id,
        block,
    )


    if updated_block is None:
        raise HTTPException(
            status_code=404,
            detail="Document block not found",
        )


    return updated_block



# ==========================================================
# Delete block
# ==========================================================

@router.delete(
    "/{block_id}",
)
def delete_block(
    block_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a document block.
    """


    deleted = document_block_service.delete_block(
        db,
        block_id,
    )


    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document block not found",
        )


    return {
        "message": "Document block deleted successfully"
    }