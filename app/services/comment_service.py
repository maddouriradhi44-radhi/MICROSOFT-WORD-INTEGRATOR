"""
Comment service.

This module contains business logic
related to section comments.
"""

from sqlalchemy.orm import Session
from app.models.user import User

from app.services.mention_parser import extract_mentions
from app.services.comment_mention_service import CommentMentionService

from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.enums.comment_status import CommentStatus


class CommentService:
    """
    Service responsible for comment management.
    """

    def __init__(self):
        self.repository = CommentRepository()
        self.mention_service = CommentMentionService()

    def create_comment(
        self,
        db: Session,
        section_id: int,
        author_id: int,
        content: str,
        parent_id: int | None = None,
    ) -> Comment:
        """
        Create a new comment on a section
        and create mentions found in its content.
        """

        comment = Comment(
            section_id=section_id,
            author_id=author_id,
            content=content,
            parent_id=parent_id,
            status=CommentStatus.OPEN,
        )

        comment = self.repository.create_comment(
            db,
            comment,
        )

        mentioned_names = extract_mentions(content)

        for name in mentioned_names:

            user = (
                db.query(User)
                .filter(
                    User.first_name.ilike(name)
                )
                .first()
            )

            if user is None:
                continue

            self.mention_service.create_mention(
                db,
                comment_id=comment.id,
                user_id=user.id,
            )

        return comment

    def update_comment(
        self,
        db: Session,
        comment_id: int,
        author_id: int,
        content: str,
    ) -> Comment | None:
        """
        Update an existing comment.

        Only the author of the comment can update it.
        """

        comment = self.repository.get_comment_by_id(
            db,
            comment_id,
        )

        if comment is None:
            return None

        if comment.author_id != author_id:
            raise PermissionError(
                "You can only update your own comments"
            )

        return self.repository.update_comment(
            db,
            comment,
            content,
        )

    def delete_comment(
        self,
        db: Session,
        comment_id: int,
        author_id: int,
    ) -> bool:
        """
        Delete a comment.

        Only the author of the comment can delete it.
        """

        comment = self.repository.get_comment_by_id(
            db,
            comment_id,
        )

        if comment is None:
            return False

        if comment.author_id != author_id:
            raise PermissionError(
                "You can only delete your own comments"
            )

        self.repository.delete_comment(
            db,
            comment,
        )

        return True

    def resolve_comment(
        self,
        db: Session,
        comment_id: int,
    ) -> Comment | None:
        """
        Resolve a comment.
        """

        comment = self.repository.get_comment_by_id(
            db,
            comment_id,
        )

        if comment is None:
            return None

        return self.repository.resolve_comment(
            db,
            comment,
        )
