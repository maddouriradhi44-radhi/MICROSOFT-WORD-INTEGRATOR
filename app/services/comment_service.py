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

from app.enums.notification_type import NotificationType
from app.enums.notification_level import NotificationLevel
from app.services.notifications_service import NotificationService

from app.repositories.section_repository import SectionRepository
from app.repositories.project_member_repository import ProjectMemberRepository

class CommentService:
    """
    Service responsible for comment management.
    """

    def __init__(self):
        self.repository = CommentRepository()
        self.mention_service = CommentMentionService()
        self.notification_service = NotificationService()
        self.section_repository = SectionRepository()

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

        # ==================================================
        # NOTIFICATION — NEW COMMENT
        # ==================================================

        section = self.section_repository.get_section_by_id(
            db,
            section_id,
        )

        if section is not None:

            project_manager = (
                ProjectMemberRepository.get_project_manager(
                    db,
                    section.project_id,
                )
            )

            notification_users = set()

            # ----------------------------------------------
            # Project Manager
            # ----------------------------------------------

            if (
                project_manager is not None
                and project_manager.user_id != author_id
            ):
                notification_users.add(
                    project_manager.user_id
                )

            # ----------------------------------------------
            # Assigned Collaborator
            # ----------------------------------------------

            if (
                section.assigned_user_id is not None
                and section.assigned_user_id != author_id
            ):
                notification_users.add(
                    section.assigned_user_id
                )

            # ----------------------------------------------
            # Send notifications
            # ----------------------------------------------

            for recipient_id in notification_users:

                self.notification_service.create_notification(
                    db=db,
                    user_id=recipient_id,
                    title="New Comment",
                    message=(
                        f'A new comment has been added '
                        f'to the section "{section.title}".'
                    ),
                    notification_type=NotificationType.COMMENT,
                    level=NotificationLevel.INFO,
                    entity_type="comment",
                    entity_id=comment.id,
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

            mention = self.mention_service.create_mention(
                db,
                comment_id=comment.id,
                user_id=user.id,
            )

            # ==================================================
            # NOTIFICATION — MENTION
            # ==================================================

            if user.id != author_id:

                self.notification_service.create_notification(
                    db=db,
                    user_id=user.id,
                    title="You Were Mentioned",
                    message=(
                        f'You were mentioned in a comment '
                        f'on the section "{section.title}".'
                    ),
                    notification_type=NotificationType.MENTION,
                    level=NotificationLevel.INFO,
                    entity_type="comment",
                    entity_id=comment.id,
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
