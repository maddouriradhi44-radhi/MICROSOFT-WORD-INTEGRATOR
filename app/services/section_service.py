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


class SectionService:
    """
    Business logic related to sections.
    """


    def __init__(self):
        self.repository = SectionRepository()
        self.notification_service = NotificationService()


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
        """


        section = self.repository.get_section_by_id(
            db,
            section_id,
        )


        if section is None:
            return None



        PermissionService.check_section_editor(
            db,
            section,
            user_id,
        )



        updates = section_data.model_dump(
            exclude_unset=True
        )



        return self.repository.update_section(
            db,
            section,
            updates,
        )

    

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
    # CREATE SECTIONS (BULK, FROM DOCX ANALYZER)
    # ======================================================

    def create_sections(
        self,
        db: Session,
        document_id: int,
        project_id: int,
        sections_data: list,
    ):
        """
        Create sections extracted from DOCX analyzer.
        """

        sections = []

        for index, section_data in enumerate(sections_data):

            section = Section(
                document_id=document_id,
                project_id=project_id,

                title=section_data["title"],

                content=section_data["content"],

                level=section_data.get("level", 1),

                order=index + 1,

                module=section_data.get("module", "general"),

            )

            sections.append(section)


        return self.repository.create_many(
            db,
            sections,
        )


    def assign_section(
        self,
        db: Session,
        section_id: int,
        assigned_user_id: int,
        current_user_id: int,
    ) -> Section | None:
        """
        Assign a section to a collaborator.

        Rules:
        - Only PROJECT_MANAGER can assign.
        - Assigned user must belong to project.
        - READER cannot receive sections.
        """

        section = self.repository.get_section_by_id(
            db,
            section_id,
        )

        if section is None:
            return None

        # Current user must be project manager
        PermissionService.check_project_manager(
            db,
            section.project_id,
            current_user_id,
        )

        # Check assigned user membership
        member = ProjectMemberRepository.get_by_project_and_user(
            db,
            section.project_id,
            assigned_user_id,
        )

        if member is None:
            raise PermissionDeniedException()

        # Reader cannot receive sections
        if member.role == ProjectRole.READER:
            raise PermissionDeniedException()

        # Assign section
        updated_section = self.repository.update_section(
            db,
            section,
            {
                "assigned_user_id": assigned_user_id,
            },
        )

        # Create notification for assigned user
        self.notification_service.create_notification(
            db=db,
            user_id=assigned_user_id,
            title="Section assignée",
            message=f"La section '{section.title}' vous a été assignée.",
            notification_type=NotificationType.SECTION,
            level=NotificationLevel.INFO,
            entity_type="section",
            entity_id=section.id,
        )

        return updated_section