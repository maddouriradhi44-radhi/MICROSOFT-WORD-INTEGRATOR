"""
Comment schemas.

This module defines Pydantic schemas
for section comments.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.comment_status import CommentStatus


class CommentCreate(BaseModel):
    """
    Schema used to create a comment or reply.
    """

    section_id: int
    content: str
    parent_id: int | None = None


class CommentUpdate(BaseModel):
    """
    Schema used to update a comment.
    """

    content: str


class CommentResponse(BaseModel):
    """
    Schema returned by API.
    """

    id: int
    content: str
    section_id: int
    author_id: int
    parent_id: int | None
    status: CommentStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class CommentListResponse(BaseModel):
    """
    Response containing multiple comments.
    """

    comments: list[CommentResponse]

