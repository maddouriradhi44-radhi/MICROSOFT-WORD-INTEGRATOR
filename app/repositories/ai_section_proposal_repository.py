"""
AI section proposal repository.

This module handles database operations
related to AI-generated section proposals.
"""

from sqlalchemy.orm import Session

from app.models.ai_section_proposal import AISectionProposal


class AISectionProposalRepository:
    """
    Database operations related to AI section proposals.
    """

    def create(
        self,
        db: Session,
        proposal: AISectionProposal,
    ) -> AISectionProposal:
        """
        Save a new AI section proposal.
        """

        db.add(proposal)
        db.commit()
        db.refresh(proposal)

        return proposal

    def get_by_id(
        self,
        db: Session,
        proposal_id: int,
    ) -> AISectionProposal | None:
        """
        Retrieve an AI proposal by its ID.
        """

        return (
            db.query(AISectionProposal)
            .filter(
                AISectionProposal.id == proposal_id
            )
            .first()
        )

    def get_by_section(
        self,
        db: Session,
        section_id: int,
    ) -> list[AISectionProposal]:
        """
        Retrieve all AI proposals for a section.
        """

        return (
            db.query(AISectionProposal)
            .filter(
                AISectionProposal.section_id == section_id
            )
            .order_by(
                AISectionProposal.id.desc()
            )
            .all()
        )

    def get_by_document(
        self,
        db: Session,
        document_id: int,
    ) -> list[AISectionProposal]:
        """
        Retrieve all AI proposals for a document.
        """

        return (
            db.query(AISectionProposal)
            .filter(
                AISectionProposal.document_id == document_id
            )
            .order_by(
                AISectionProposal.id
            )
            .all()
        )
    # ==========================================================
    # UPDATE PROPOSAL
    # ==========================================================

    def update(
        self,
        db: Session,
        proposal: AISectionProposal,
    ) -> AISectionProposal:
        """
        Update an AI section proposal.
        """

        db.add(proposal)
        db.commit()
        db.refresh(proposal)

        return proposal

    # ==========================================================
    # GET PENDING PROPOSALS
    # ==========================================================

    def get_pending_by_document(
        self,
        db: Session,
        document_id: int,
    ) -> list[AISectionProposal]:
        """
        Retrieve pending AI proposals for a document.
        """

        return (
            db.query(AISectionProposal)
            .filter(
                AISectionProposal.document_id == document_id,
                AISectionProposal.status == "PENDING",
            )
            .order_by(
                AISectionProposal.order
            )
            .all()
        )