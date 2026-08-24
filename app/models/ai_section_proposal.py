"""
AI section proposal model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.section import Section
    from app.models.user import User

from datetime import datetime

from app.enums.ai_proposal_status import AIProposalStatus


class AISectionProposal(Base):
    """
    Represents an AI-generated proposal for a logical
    section of a document.

    The proposal exists before the real Section is created.
    The Project Manager must validate the proposal first.
    """

    __tablename__ = "ai_section_proposals"

    # ======================================================
    # IDENTIFICATION
    # ======================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # ======================================================
    # DOCUMENT
    # ======================================================

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    # ======================================================
    # CREATED SECTION
    # ======================================================

    section_id: Mapped[int | None] = mapped_column(
        ForeignKey("sections.id"),
        nullable=True,
    )

    # ======================================================
    # PROPOSAL STRUCTURE
    # ======================================================

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
    )

    level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    order: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ======================================================
    # AI ANALYSIS
    # ======================================================

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    suggested_role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    keywords: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    complexity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="medium",
    )

    # ======================================================
    # PROJECT MANAGER DECISION
    # ======================================================

    # ======================================================
    # PROPOSAL STATUS
    # ======================================================

    status: Mapped[AIProposalStatus] = mapped_column(
        Enum(
            AIProposalStatus,
            name="ai_proposal_status",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=AIProposalStatus.PENDING,
    )

    reviewed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    review_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    document: Mapped["Document"] = relationship()

    section: Mapped["Section | None"] = relationship()

    reviewer: Mapped["User | None"] = relationship()