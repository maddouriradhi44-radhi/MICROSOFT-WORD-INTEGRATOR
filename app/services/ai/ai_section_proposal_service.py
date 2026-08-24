"""
AI section proposal service.

This module handles the creation, retrieval,
modification, acceptance and rejection of
AI-generated section proposals.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ai_section_proposal import AISectionProposal
from app.models.section import Section

from app.repositories.ai_section_proposal_repository import (
    AISectionProposalRepository,
)

from app.schemas.ai import (
    AISectionProposal as AISectionProposalSchema,
)

from app.enums.ai_proposal_status import AIProposalStatus

from app.services.permission_service import PermissionService

from app.models.document_block import DocumentBlock
from app.services.docx_analyzer_service import DocxAnalyzerService
from app.services.storage_service import StorageService


class AISectionProposalService:
    """
    Service responsible for AI section proposals.
    """

    def __init__(self):
        self.repository = AISectionProposalRepository()

    # ==========================================================
    # CREATE PROPOSAL
    # ==========================================================

    def create_proposal(
        self,
        db: Session,
        document_id: int,
        proposal: AISectionProposalSchema,
    ) -> AISectionProposal:
        """
        Save an AI-generated section proposal.

        The proposal does not create a real Section.
        The Project Manager must review it first.
        """

        db_proposal = AISectionProposal(
            document_id=document_id,
            section_id=None,
            title=proposal.title,
            content=proposal.content,
            level=proposal.level,
            order=proposal.order,
            reason=proposal.reason,
            confidence=proposal.confidence,
            category=proposal.category,
            suggested_role=proposal.suggested_role,
            keywords=",".join(proposal.keywords),
            complexity=proposal.complexity,
        )

        return self.repository.create(
            db,
            db_proposal,
        )

    # ==========================================================
    # GET SECTION PROPOSALS
    # ==========================================================

    def get_section_proposals(
        self,
        db: Session,
        section_id: int,
    ) -> list[AISectionProposal]:
        """
        Retrieve AI proposals for a section.
        """

        return self.repository.get_by_section(
            db,
            section_id,
        )

    # ==========================================================
    # GET DOCUMENT PROPOSALS
    # ==========================================================

    def get_document_proposals(
        self,
        db: Session,
        document_id: int,
    ) -> list[AISectionProposal]:
        """
        Retrieve AI proposals for a document.
        """

        return self.repository.get_by_document(
            db,
            document_id,
        )

    # ==========================================================
    # GET PROPOSAL BY ID
    # ==========================================================

    def get_proposal_by_id(
        self,
        db: Session,
        proposal_id: int,
    ) -> AISectionProposal | None:
        """
        Retrieve a proposal by ID.
        """

        return self.repository.get_by_id(
            db,
            proposal_id,
        )

    # ==========================================================
    # UPDATE PROPOSAL
    # ==========================================================

    def update_proposal(
        self,
        db: Session,
        proposal_id: int,
        user_id: int,
        title: str | None = None,
        content: str | None = None,
        level: int | None = None,
        order: int | None = None,
        category: str | None = None,
        suggested_role: str | None = None,
        keywords: list[str] | None = None,
        complexity: str | None = None,
        review_comment: str | None = None,
    ) -> AISectionProposal:
        """
        Modify an AI proposal before acceptance or rejection.

        Only the Project Manager can modify a proposal.
        """

        proposal = self.repository.get_by_id(
            db,
            proposal_id,
        )

        if proposal is None:
            raise ValueError("AI proposal not found")

        if proposal.status != AIProposalStatus.PENDING:
            raise ValueError(
                "Only pending AI proposals can be modified"
            )

        document = proposal.document

        if document is None:
            raise ValueError("Document not found")

        # ------------------------------------------------------
        # PROJECT MANAGER PERMISSION
        # ------------------------------------------------------

        PermissionService.check_project_manager(
            db=db,
            project_id=document.project_id,
            user_id=user_id,
        )

        # ------------------------------------------------------
        # UPDATE FIELDS
        # ------------------------------------------------------

        if title is not None:
            proposal.title = title

        if content is not None:
            proposal.content = content

        if level is not None:
            proposal.level = level

        if order is not None:
            proposal.order = order

        if category is not None:
            proposal.category = category

        if suggested_role is not None:
            proposal.suggested_role = suggested_role

        if keywords is not None:
            proposal.keywords = ",".join(
                keyword.strip()
                for keyword in keywords
                if keyword.strip()
            )

        if complexity is not None:
            proposal.complexity = complexity

        if review_comment is not None:
            proposal.review_comment = review_comment

        db.commit()
        db.refresh(proposal)

        return proposal

    # ==========================================================
    # ACCEPT PROPOSAL
    # ==========================================================

    def accept_proposal(
        self,
        db: Session,
        proposal_id: int,
        user_id: int,
        assigned_user_id: int | None = None,
    ) -> Section:
        """
        Accept an AI proposal and create the real Section.

        Only the Project Manager can accept a proposal.
        """

        proposal = self.repository.get_by_id(
            db,
            proposal_id,
        )

        if proposal is None:
            raise ValueError("AI proposal not found")

        if proposal.status != AIProposalStatus.PENDING:
            raise ValueError(
                "AI proposal has already been reviewed"
            )

        document = proposal.document

        if document is None:
            raise ValueError("Document not found")

        # ------------------------------------------------------
        # PROJECT MANAGER PERMISSION
        # ------------------------------------------------------

        PermissionService.check_project_manager(
            db=db,
            project_id=document.project_id,
            user_id=user_id,
        )

        # ------------------------------------------------------
        # CREATE REAL SECTION
        # ------------------------------------------------------

        section = Section(
            title=proposal.title,
            content=proposal.content,
            level=proposal.level or 1,
            order=proposal.order or 0,
            module=proposal.category or "general",
            document_id=proposal.document_id,
            project_id=document.project_id,
            assigned_user_id=assigned_user_id,
        )

        db.add(section)
        db.flush()

        # ------------------------------------------------------
        # CREATE DOCUMENT BLOCKS
        # ------------------------------------------------------

        storage_service = StorageService()

        original_path = storage_service.get_absolute_path(
            document.storage_key
        )

        analyzer = DocxAnalyzerService()

        analyzed_sections = analyzer.analyze(
            original_path
        )

        # Match the AI proposal with the original
        # logical section using its order.
        source_section = None

        if proposal.order is not None:
            source_index = proposal.order - 1

            if 0 <= source_index < len(analyzed_sections):
                source_section = analyzed_sections[source_index]

        print(
            "DEBUG AI ACCEPT:",
            "proposal_order=", proposal.order,
            "analyzed_sections=", len(analyzed_sections),
            "source_section=", source_section,
        )

        if source_section is not None:

            for block_data in source_section.get(
                "blocks",
                [],
            ):

                block = DocumentBlock(
                    section_id=section.id,
                    type=block_data["type"],
                    content_xml=block_data["content_xml"],
                    order_index=block_data["order_index"],
                )

                db.add(block)

        else:

            # Fallback: create a textual block
            # from the accepted AI proposal.
            block = DocumentBlock(
                section_id=section.id,
                type="paragraph",
                content_xml=proposal.content,
                order_index=0.0,
            )

            db.add(block)

        # ------------------------------------------------------
        # UPDATE PROPOSAL
        # ------------------------------------------------------

        proposal.status = AIProposalStatus.ACCEPTED
        proposal.section_id = section.id
        proposal.reviewed_by = user_id
        proposal.reviewed_at = datetime.utcnow()

        db.commit()
        db.refresh(section)

        return section

    # ==========================================================
    # REJECT PROPOSAL
    # ==========================================================

    def reject_proposal(
        self,
        db: Session,
        proposal_id: int,
        user_id: int,
        review_comment: str | None = None,
    ) -> AISectionProposal:
        """
        Reject an AI proposal.

        Rejection does not create a Section.
        """

        proposal = self.repository.get_by_id(
            db,
            proposal_id,
        )

        if proposal is None:
            raise ValueError("AI proposal not found")

        if proposal.status != AIProposalStatus.PENDING:
            raise ValueError(
                "AI proposal has already been reviewed"
            )

        document = proposal.document

        if document is None:
            raise ValueError("Document not found")

        # ------------------------------------------------------
        # PROJECT MANAGER PERMISSION
        # ------------------------------------------------------

        PermissionService.check_project_manager(
            db=db,
            project_id=document.project_id,
            user_id=user_id,
        )

        # ------------------------------------------------------
        # REJECT
        # ------------------------------------------------------

        proposal.status = AIProposalStatus.REJECTED
        proposal.reviewed_by = user_id
        proposal.reviewed_at = datetime.utcnow()
        proposal.review_comment = review_comment

        db.commit()
        db.refresh(proposal)

        return proposal