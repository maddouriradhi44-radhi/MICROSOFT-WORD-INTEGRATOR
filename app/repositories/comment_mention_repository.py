"""
Comment mention repository.

This module contains database operations
related to comment mentions.
"""

from sqlalchemy.orm import Session

from app.models.comment_mention import CommentMention


class CommentMentionRepository:
    """
    Repository responsible for comment mention database operations.
    """

    def create_mention(
        self,
        db: Session,
        mention: CommentMention,
    ) -> CommentMention:
        """
        Create a new comment mention.
        """

        db.add(mention)
        db.commit()
        db.refresh(mention)

        return mention

    def get_comment_mentions(
        self,
        db: Session,
        comment_id: int,
    ) -> list[CommentMention]:
        """
        Retrieve all mentions of a comment.
        """

        return (
            db.query(CommentMention)
            .filter(
                CommentMention.comment_id == comment_id
            )
            .all()
        )

    def get_user_mentions(
        self,
        db: Session,
        user_id: int,
    ) -> list[CommentMention]:
        """
        Retrieve all mentions of a user.
        """

        return (
            db.query(CommentMention)
            .filter(
                CommentMention.user_id == user_id
            )
            .all()
        )

    def delete_mention(
        self,
        db: Session,
        mention: CommentMention,
    ) -> None:
        """
        Delete a comment mention.
        """

        db.delete(mention)
        db.commit()