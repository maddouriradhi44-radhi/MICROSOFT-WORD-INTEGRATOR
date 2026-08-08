"""
Comment API routes.

This module exposes endpoints
for section comments.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.database.session import get_db

from app.models.user import User

from app.schemas.comment_schema import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentListResponse,
)

from app.services.comment_service import CommentService

from app.dependencies.auth_dependency import get_current_user



router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


comment_service = CommentService()

@router.post(
    "",
    response_model=CommentResponse,
)
def create_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a comment on a section.
    """


    return comment_service.create_comment(
        db,
        section_id=data.section_id,
        author_id=current_user.id,
        content=data.content,
        parent_id=data.parent_id,
    )


@router.get(
    "/section/{section_id}",
    response_model=CommentListResponse,
)
def get_section_comments(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve comments of a section.
    """


    comments = comment_service.get_section_comments(
        db,
        section_id,
    )


    return {
        "comments": comments
    }


@router.patch(
    "/{comment_id}",
    response_model=CommentResponse,
)
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a comment.

    Only the author can update the comment.
    """

    try:
        comment = comment_service.update_comment(
            db,
            comment_id,
            author_id=current_user.id,
            content=data.content,
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    return comment


@router.delete(
    "/{comment_id}",
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a comment.

    Only the author can delete the comment.
    """

    try:
        deleted = comment_service.delete_comment(
            db,
            comment_id,
            author_id=current_user.id,
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    return {
        "message": "Comment deleted successfully"
    }



@router.patch(
    "/{comment_id}/resolve",
    response_model=CommentResponse,
)
def resolve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):


    comment = comment_service.resolve_comment(
        db,
        comment_id,
    )


    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )


    return comment