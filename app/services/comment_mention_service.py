"""
Comment mention service.

This module contains business logic
related to comment mentions.
"""

from sqlalchemy.orm import Session

from app.models.comment_mention import CommentMention
from app.repositories.comment_mention_repository import (
    CommentMentionRepository,
)


class CommentMentionService:
    """
    Service responsible for comment mention management.
    """

    def __init__(self):
        self.repository = CommentMentionRepository()

    def create_mention(
        self,
        db: Session,
        comment_id: int,
        user_id: int,
    ) -> CommentMention:
        """
        Create a mention for a user in a comment.
        """

        mention = CommentMention(
            comment_id=comment_id,
            user_id=user_id,
        )

        return self.repository.create_mention(
            db,
            mention,
        )

    def get_comment_mentions(
        self,
        db: Session,
        comment_id: int,
    ) -> list[CommentMention]:
        """
        Retrieve all users mentioned in a comment.
        """

        return self.repository.get_comment_mentions(
            db,
            comment_id,
        )

    def get_user_mentions(
        self,
        db: Session,
        user_id: int,
    ) -> list[CommentMention]:
        """
        Retrieve all comments mentioning a user.
        """

        return self.repository.get_user_mentions(
            db,
            user_id,
        )

    def delete_mention(
        self,
        db: Session,
        mention: CommentMention,
    ) -> None:
        """
        Delete a comment mention.
        """

        self.repository.delete_mention(
            db,
            mention,
        )