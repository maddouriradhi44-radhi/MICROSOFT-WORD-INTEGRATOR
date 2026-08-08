"""
Comment repository.

This module handles database operations
related to section comments.
"""

from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    """
    Repository responsible for Comment database operations.
    """


    def create_comment(
        self,
        db: Session,
        comment: Comment,
    ) -> Comment:
        """
        Create a new comment.
        """

        db.add(comment)

        db.commit()

        db.refresh(comment)

        return comment



    def get_comment_by_id(
        self,
        db: Session,
        comment_id: int,
    ) -> Comment | None:
        """
        Retrieve a comment by id.
        """

        return (
            db.query(Comment)
            .filter(
                Comment.id == comment_id
            )
            .first()
        )



    def get_section_comments(
        self,
        db: Session,
        section_id: int,
    ) -> list[Comment]:
        """
        Retrieve all comments
        belonging to a section.
        """

        return (
            db.query(Comment)
            .filter(
                Comment.section_id == section_id
            )
            .order_by(
                Comment.created_at.asc()
            )
            .all()
        )



    def update_comment(
        self,
        db: Session,
        comment: Comment,
        content: str,
    ) -> Comment:
        """
        Update comment content.
        """

        comment.content = content

        db.commit()

        db.refresh(comment)

        return comment



    def delete_comment(
        self,
        db: Session,
        comment: Comment,
    ) -> None:
        """
        Delete a comment.
        """

        db.delete(comment)

        db.commit()



    def resolve_comment(
        self,
        db: Session,
        comment: Comment,
    ) -> Comment:
        """
        Mark a comment as resolved.
        """

        from app.enums.comment_status import CommentStatus

        comment.status = CommentStatus.RESOLVED

        db.commit()

        db.refresh(comment)

        return comment