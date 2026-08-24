"""
AI validation report model.

Stores the AI analysis performed on a section version
before Project Manager validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.ai_analysis_status import AIAnalysisStatus


if TYPE_CHECKING:
    from app.models.validation import Validation


class AIValidationReport(Base):
    """
    Represents the AI analysis report associated
    with a pending validation.
    """

    __tablename__ = "ai_validation_reports"

    # ==========================================================
    # PRIMARY KEY
    # ==========================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # ==========================================================
    # VALIDATION
    # ==========================================================

    validation_id: Mapped[int] = mapped_column(
        ForeignKey("validations.id"),
        nullable=False,
        unique=True,
    )

    # ==========================================================
    # AI ANALYSIS STATUS
    # ==========================================================

    analysis_status: Mapped[AIAnalysisStatus] = mapped_column(
        String(20),
        default=AIAnalysisStatus.PENDING.value,
        nullable=False,
    )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # CHANGE COUNTS
    # ==========================================================

    addition_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    deletion_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    modification_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ==========================================================
    # IMPORTANT CHANGES
    # ==========================================================

    important_changes: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # ==========================================================
    # RISKS
    # ==========================================================

    risks: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    confidence_level: Mapped[str] = mapped_column(
        String(20),
        default="low",
        nullable=False,
    )

    # ==========================================================
    # COHERENCE
    # ==========================================================

    coherence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    coherence_level: Mapped[str] = mapped_column(
        String(20),
        default="critical",
        nullable=False,
    )

    coherence_issues: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    coherence_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # RECOMMENDATION
    # ==========================================================

    recommendation: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    recommendation_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # ==========================================================
    # RELATIONSHIP
    # ==========================================================

    validation: Mapped[Validation] = relationship(
        back_populates="ai_report",
    )