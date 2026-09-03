"""
Section service.

This module contains business logic
related to document sections.
"""

from sqlalchemy.orm import Session

from app.models.section import Section

from app.repositories.section_repository import (
    SectionRepository,
)

from app.repositories.document_repository import DocumentRepository

from app.repositories.project_member_repository import (
    ProjectMemberRepository,
)

from app.schemas.section_schema import (
    SectionCreate,
    SectionUpdate,
)

from app.enums.project_role import ProjectRole

from app.services.permission_service import (
    PermissionService,
)

from app.exceptions.permission import (
    PermissionDeniedException,
)

from app.enums.notification_type import NotificationType
from app.enums.notification_level import NotificationLevel
from app.services.notifications_service import NotificationService

from app.models.document_block import DocumentBlock


class SectionService:
    """
    Business logic related to sections.
    """

    def __init__(self):
        self.repository = SectionRepository()
        self.notification_service = NotificationService()

    # ======================================================
    # SECTION NOTIFICATION USERS
    # ======================================================

    def _get_section_notification_users(
        self,
        db: Session,
        section: Section,
        exclude_user_id: int | None = None,
    ) -> list[int]:
        """
        Retrieve users who should receive notifications
        related to a section.

        Current recipients:
        - Project Manager
        - Assigned collaborator

        The user who performed the action can be excluded.
        """

        user_ids = set()

        # --------------------------------------------------
        # Project Manager
        # --------------------------------------------------

        project_manager = (
            ProjectMemberRepository.get_project_manager(
                db,
                section.project_id,
            )
        )

        if (
            project_manager is not None
            and project_manager.user_id != exclude_user_id
        ):
            user_ids.add(project_manager.user_id)

        # --------------------------------------------------
        # Assigned collaborator
        # --------------------------------------------------

        if (
            section.assigned_user_id is not None
            and section.assigned_user_id != exclude_user_id
        ):
            user_ids.add(section.assigned_user_id)

        return list(user_ids)

    # ======================================================
    # CREATE SECTION
    # ======================================================

    def create_section(
        self,
        db: Session,
        section_data: SectionCreate,
        user_id: int,
    ) -> Section:
        """
        Create a new section.

        Only PROJECT_MANAGER can create sections.
        """

        PermissionService.check_project_manager(
            db,
            section_data.project_id,
            user_id,
        )

        document = DocumentRepository().get_document_by_id(
            db,
            section_data.document_id,
        )

        if document is None:
            raise ValueError("Document not found")

        if document.project_id != section_data.project_id:
            raise PermissionDeniedException()

        section = Section(
            title=section_data.title,
            content=section_data.content,
            level=section_data.level,
            order=section_data.order,
            module=section_data.module,
            document_id=section_data.document_id,
            project_id=section_data.project_id,
            assigned_user_id=section_data.assigned_user_id,
        )

        return self.repository.create_section(
            db,
            section,
        )

    # ======================================================
    # GET SECTION BY ID
    # ======================================================

    def get_section_by_id(
        self,
        db: Session,
        section_id: int,
    ) -> Section | None:
        """
        Retrieve section by id.
        """

        return self.repository.get_section_by_id(
            db,
            section_id,
        )

    # ======================================================
    # GET DOCUMENT SECTIONS
    # ======================================================

    def get_document_sections(
        self,
        db: Session,
        document_id: int,
    ) -> list[Section]:
        """
        Retrieve all sections belonging to a document.
        """

        return self.repository.get_document_sections(
            db,
            document_id,
        )

    # ======================================================
    # GET USER SECTIONS
    # ======================================================

    def get_user_sections(
        self,
        db: Session,
        user_id: int,
    ) -> list[Section]:
        """
        Retrieve sections assigned to a user.
        """

        return self.repository.get_user_sections(
            db,
            user_id,
        )

    # ======================================================
    # UPDATE SECTION
    # ======================================================

    def update_section(
        self,
        db: Session,
        section_id: int,
        section_data: SectionUpdate,
        user_id: int,
    ) -> Section | None:
        """
        Update a section.

        Rules:
        - PROJECT_MANAGER can update all sections.
        - COLLABORATOR can update only his assigned section.
        - Notifications are sent only when a real change occurs.
        - The user performing the modification does not receive
          a notification about their own modification.
        """

        # --------------------------------------------------
        # Get section
        # --------------------------------------------------

        section = self.repository.get_section_by_id(
            db,
            section_id,
        )

        if section is None:
            return None

        # --------------------------------------------------
        # Permission check
        # --------------------------------------------------

        PermissionService.check_section_editor(
            db,
            section,
            user_id,
        )

        # --------------------------------------------------
        # Get requested updates
        # --------------------------------------------------

        updates = section_data.model_dump(
            exclude_unset=True
        )

        if not updates:
            return section

        # --------------------------------------------------
        # Save old values
        # --------------------------------------------------

        old_title = section.title
        old_content = section.content
        old_status = section.status
        old_assigned_user_id = section.assigned_user_id

        # --------------------------------------------------
        # Detect real changes
        # --------------------------------------------------

        title_changed = (
            "title" in updates
            and updates["title"] != old_title
        )

        content_changed = (
            "content" in updates
            and updates["content"] != old_content
        )

        status_changed = (
            "status" in updates
            and updates["status"] != old_status
        )

        assignment_changed = (
            "assigned_user_id" in updates
            and updates["assigned_user_id"]
            != old_assigned_user_id
        )

        # --------------------------------------------------
        # Nothing actually changed
        # --------------------------------------------------

        if not (
            title_changed
            or content_changed
            or status_changed
            or assignment_changed
        ):
            return section

        # --------------------------------------------------
        # Update section
        # --------------------------------------------------

        updated_section = self.repository.update_section(
            db,
            section,
            updates,
        )

        # ==================================================
        # ASSIGNMENT CHANGE
        # ==================================================

        if assignment_changed:

            new_assigned_user_id = updates["assigned_user_id"]

            # ----------------------------------------------
            # Notify old collaborator
            # ----------------------------------------------

            if old_assigned_user_id is not None:

                self.notification_service.create_notification(
                    db=db,
                    user_id=old_assigned_user_id,
                    title="Section Assignment Removed",
                    message=(
                        f'The section "{old_title}" is no longer '
                        "assigned to you. You no longer have access "
                        "to edit this section."
                    ),
                    notification_type=NotificationType.SECTION,
                    level=NotificationLevel.INFO,
                    entity_type="section",
                    entity_id=section.id,
                )

            # ----------------------------------------------
            # Notify new collaborator
            # ----------------------------------------------

            if (
                new_assigned_user_id is not None
                and new_assigned_user_id != user_id
            ):

                self.notification_service.create_notification(
                    db=db,
                    user_id=new_assigned_user_id,
                    title="Section Assigned",
                    message=(
                        f'The section "{updated_section.title}" '
                        "has been assigned to you."
                    ),
                    notification_type=NotificationType.SECTION,
                    level=NotificationLevel.INFO,
                    entity_type="section",
                    entity_id=section.id,
                )

            # ----------------------------------------------
            # Notify Project Manager
            # ----------------------------------------------

            project_manager = (
                ProjectMemberRepository.get_project_manager(
                    db,
                    section.project_id,
                )
            )

            if (
                project_manager is not None
                and project_manager.user_id != user_id
                and project_manager.user_id != new_assigned_user_id
            ):

                self.notification_service.create_notification(
                    db=db,
                    user_id=project_manager.user_id,
                    title="Section Reassigned",
                    message=(
                        f'The section "{updated_section.title}" '
                        "has been reassigned."
                    ),
                    notification_type=NotificationType.SECTION,
                    level=NotificationLevel.INFO,
                    entity_type="section",
                    entity_id=section.id,
                )

        # ==================================================
        # TITLE / CONTENT / STATUS CHANGE
        # ==================================================

        if (
            title_changed
            or content_changed
            or status_changed
        ):

            notification_users = (
                self._get_section_notification_users(
                    db,
                    updated_section,
                    exclude_user_id=user_id,
                )
            )

            changes = []

            if title_changed:
                changes.append("title")

            if content_changed:
                changes.append("content")

            if status_changed:
                changes.append("status")

            changes_text = ", ".join(changes)

            for recipient_id in notification_users:

                self.notification_service.create_notification(
                    db=db,
                    user_id=recipient_id,
                    title="Section Updated",
                    message=(
                        f'The section "{updated_section.title}" '
                        f'has been updated ({changes_text}).'
                    ),
                    notification_type=NotificationType.SECTION,
                    level=NotificationLevel.INFO,
                    entity_type="section",
                    entity_id=section.id,
                )

        return updated_section

    # ======================================================
    # DELETE SECTION
    # ======================================================

    def delete_section(
        self,
        db: Session,
        section_id: int,
        user_id: int,
    ) -> bool:
        """
        Delete section.

        Only PROJECT_MANAGER can delete.
        """

        section = self.repository.get_section_by_id(
            db,
            section_id,
        )

        if section is None:
            return False

        PermissionService.check_project_manager(
            db,
            section.project_id,
            user_id,
        )

        self.repository.delete_section(
            db,
            section,
        )

        return True

    # ======================================================
    # CREATE SECTIONS
    # BULK - FROM DOCX ANALYZER
    # ======================================================

    def create_sections(
        self,
        db: Session,
        document_id: int,
        project_id: int,
        sections_data: list,
    ):
        """
        Create sections and their document blocks
        extracted by the DOCX analyzer.
        """

        sections = []

        for index, section_data in enumerate(sections_data):

            section = Section(
                document_id=document_id,
                project_id=project_id,
                title=section_data["title"],
                content=section_data.get("content", ""),
                level=section_data.get("level", 1),
                order=index + 1,
                module=section_data.get("module", "general"),
            )

            sections.append(section)

        # Créer d'abord les sections
        created_sections = self.repository.create_many(
            db,
            sections,
        )

        # Créer les DocumentBlocks liés aux sections
        for section, section_data in zip(
            created_sections,
            sections_data,
        ):

            for block_data in section_data.get("blocks", []):

                block = DocumentBlock(
                    section_id=section.id,
                    type=block_data["type"],
                    content_xml=block_data["content_xml"],
                    order_index=block_data["order_index"],
                )

                db.add(block)

        db.commit()

        return created_sections
    # ======================================================
    # ASSIGN SECTION
    # ======================================================

    def assign_section(
        self,
        db: Session,
        section_id: int,
        assigned_user_id: int,
        current_user_id: int,
    ) -> Section | None:
        """
        Assign a section to a project member.

        Rules:
        - Only PROJECT_MANAGER can assign.
        - Assigned user must belong to the project.
        - Previous collaborator is notified when assignment changes.
        """

        # --------------------------------------------------
        # Get section
        # --------------------------------------------------

        section = self.repository.get_section_by_id(
            db,
            section_id,
        )

        if section is None:
            return None


        # --------------------------------------------------
        # Permission check
        # --------------------------------------------------

        PermissionService.check_project_manager(
            db,
            section.project_id,
            current_user_id,
        )

        # --------------------------------------------------
        # Check assigned user membership
        # --------------------------------------------------

        assigned_member = (
            ProjectMemberRepository.get_by_project_and_user(
                db,
                section.project_id,
                assigned_user_id,
            )
        )

        if assigned_member is None:
            raise PermissionDeniedException()

        # --------------------------------------------------
        # Save previous responsible user
        # BEFORE changing assignment
        # --------------------------------------------------

        previous_assigned_user_id = (
            section.assigned_user_id
        )

        # --------------------------------------------------
        # Nothing changed
        # --------------------------------------------------

        if previous_assigned_user_id == assigned_user_id:
            return section

        # --------------------------------------------------
        # Update assignment
        # --------------------------------------------------

        updated_section = self.repository.update_section(
            db,
            section,
            {
                "assigned_user_id": assigned_user_id,
            },
        )

        # ==================================================
        # NOTIFY PREVIOUS RESPONSIBLE USER
        # ==================================================

        if previous_assigned_user_id is not None:

            self.notification_service.create_notification(
                db=db,
                user_id=previous_assigned_user_id,
                title="Section Assignment Removed",
                message=(
                    f'The section "{section.title}" is no longer '
                    "assigned to you. You no longer have access "
                    "to edit this section."
                ),
                notification_type=NotificationType.SECTION,
                level=NotificationLevel.INFO,
                entity_type="section",
                entity_id=section.id,
            )

        # ==================================================
        # NOTIFY NEW RESPONSIBLE USER
        # ==================================================

        if assigned_user_id != current_user_id:

            self.notification_service.create_notification(
                db=db,
                user_id=assigned_user_id,
                title="Section Assigned",
                message=(
                    f'The section "{updated_section.title}" '
                    "has been assigned to you."
                ),
                notification_type=NotificationType.SECTION,
                level=NotificationLevel.INFO,
                entity_type="section",
                entity_id=section.id,
            )

        return updated_section


    def get_project_sections(
        self,
        db: Session,
        project_id: int,
    ) -> list[Section]:
        """
        Retrieve all sections belonging to a project.
        """

        return self.repository.get_project_sections(
            db,
            project_id,
        )