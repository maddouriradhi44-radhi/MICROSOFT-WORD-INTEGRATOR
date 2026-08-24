"""
AI analysis status service.

Responsible for managing the lifecycle of an AI validation report.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.enums.ai_analysis_status import AIAnalysisStatus
from app.models.ai_validation_report import AIValidationReport


class AIAnalysisStatusService:
    """
    Service responsible for managing AI analysis status transitions.

    Valid lifecycle:

        PENDING
            ↓
        IN_PROGRESS
            ↓
        COMPLETED

    In case of failure:

        IN_PROGRESS
            ↓
        FAILED
    """

    # ==========================================================
    # START ANALYSIS
    # ==========================================================

    @staticmethod
    def start_analysis(
        db: Session,
        report: AIValidationReport,
    ) -> AIValidationReport:
        """
        Move an AI report from PENDING to IN_PROGRESS.
        """

        if report.analysis_status != AIAnalysisStatus.PENDING:
            raise ValueError(
                "AI analysis can only start from PENDING status."
            )

        report.analysis_status = AIAnalysisStatus.IN_PROGRESS

        db.add(report)
        db.commit()
        db.refresh(report)

        return report

    # ==========================================================
    # COMPLETE ANALYSIS
    # ==========================================================

    @staticmethod
    def complete_analysis(
        db: Session,
        report: AIValidationReport,
    ) -> AIValidationReport:
        """
        Move an AI report from IN_PROGRESS to COMPLETED.
        """

        if report.analysis_status != AIAnalysisStatus.IN_PROGRESS:
            raise ValueError(
                "AI analysis can only be completed "
                "from IN_PROGRESS status."
            )

        report.analysis_status = AIAnalysisStatus.COMPLETED

        db.add(report)
        db.commit()
        db.refresh(report)

        return report

    # ==========================================================
    # FAIL ANALYSIS
    # ==========================================================

    @staticmethod
    def fail_analysis(
        db: Session,
        report: AIValidationReport,
    ) -> AIValidationReport:
        """
        Move an AI report from IN_PROGRESS to FAILED.
        """

        if report.analysis_status != AIAnalysisStatus.IN_PROGRESS:
            raise ValueError(
                "AI analysis can only fail "
                "from IN_PROGRESS status."
            )

        report.analysis_status = AIAnalysisStatus.FAILED

        db.add(report)
        db.commit()
        db.refresh(report)

        return report

    # ==========================================================
    # SET STATUS
    # ==========================================================

    @staticmethod
    def set_status(
        db: Session,
        report: AIValidationReport,
        status: AIAnalysisStatus,
    ) -> AIValidationReport:
        """
        Safely update the AI analysis status.

        This method enforces the allowed lifecycle transitions.
        """

        current_status = report.analysis_status

        allowed_transitions = {
            AIAnalysisStatus.PENDING: {
                AIAnalysisStatus.IN_PROGRESS,
            },
            AIAnalysisStatus.IN_PROGRESS: {
                AIAnalysisStatus.COMPLETED,
                AIAnalysisStatus.FAILED,
            },
            AIAnalysisStatus.COMPLETED: set(),
            AIAnalysisStatus.FAILED: set(),
        }

        if status == current_status:
            return report

        if status not in allowed_transitions.get(
            current_status,
            set(),
        ):
            raise ValueError(
                f"Invalid AI analysis status transition: "
                f"{current_status} -> {status}."
            )

        report.analysis_status = status

        db.add(report)
        db.commit()
        db.refresh(report)

        return report