"""
AI validation report service.

Orchestrates the complete AI analysis of a new section version
before Project Manager validation.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.version import Version
from app.models.validation import Validation
from app.models.ai_validation_report import AIValidationReport

from app.services.ai.ai_version_comparison_service import (
    AIVersionComparisonService,
)
from app.services.ai.ai_change_summary_service import (
    AIChangeSummaryService,
)
from app.services.ai.ai_risk_detection_service import (
    AIRiskDetectionService,
)
from app.services.ai.ai_confidence_service import (
    AIConfidenceService,
)
from app.services.ai.ai_recommendation_service import (
    AIRecommendationService,
)
from app.services.ai.ai_coherence_service import (
    AICoherenceService,
)
from app.services.ai.ai_analysis_status_service import (
    AIAnalysisStatusService,
)


class AIValidationReportService:
    """
    Service responsible for generating and storing
    the complete AI validation report.
    """

    def __init__(self):
        self.comparison_service = (
            AIVersionComparisonService()
        )

        self.summary_service = (
            AIChangeSummaryService()
        )

        self.risk_service = (
            AIRiskDetectionService()
        )

        self.confidence_service = (
            AIConfidenceService()
        )

        self.recommendation_service = (
            AIRecommendationService()
        )

        self.coherence_service = (
            AICoherenceService()
        )

        self.status_service = (
            AIAnalysisStatusService()
        )

    # ==========================================================
    # GENERATE REPORT
    # ==========================================================

    def generate_report(
        self,
        db: Session,
        validation: Validation,
    ) -> AIValidationReport:
        """
        Generate and store the complete AI report
        for a pending validation.

        Lifecycle:

            PENDING
                ↓
            IN_PROGRESS
                ↓
            COMPLETED

        On analysis failure:

            IN_PROGRESS
                ↓
            FAILED
        """

        # ------------------------------------------------------
        # EXISTING REPORT
        # ------------------------------------------------------

        existing_report = (
            db.query(AIValidationReport)
            .filter(
                AIValidationReport.validation_id
                == validation.id
            )
            .first()
        )

        if existing_report is not None:
            return existing_report

        # ------------------------------------------------------
        # VALIDATION VERSION
        # ------------------------------------------------------

        new_version = validation.version

        if new_version is None:
            raise ValueError(
                "Validation version not found."
            )

        # ------------------------------------------------------
        # PREVIOUS VERSION
        # ------------------------------------------------------

        old_version = new_version.parent_version

        if old_version is None:
            raise ValueError(
                "Previous version not found."
            )

        # ------------------------------------------------------
        # CREATE EMPTY REPORT
        # ------------------------------------------------------

        report = AIValidationReport(
            validation_id=validation.id,
            recommendation="PENDING",
            recommendation_reason="AI analysis pending",
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        # ------------------------------------------------------
        # START AI ANALYSIS
        # ------------------------------------------------------

        self.status_service.start_analysis(
            db,
            report,
        )

        try:

            # --------------------------------------------------
            # VERSION COMPARISON
            # --------------------------------------------------

            comparison = (
                self.comparison_service.compare_versions(
                    old_version=old_version,
                    new_version=new_version,
                )
            )

            # --------------------------------------------------
            # CHANGE SUMMARY
            # --------------------------------------------------

            summary_result = (
                self.summary_service.generate_summary(
                    comparison,
                )
            )

            # --------------------------------------------------
            # RISK DETECTION
            # --------------------------------------------------

            risk_result = (
                self.risk_service.detect_risks(
                    comparison,
                )
            )

            # --------------------------------------------------
            # CONFIDENCE
            # --------------------------------------------------

            confidence_result = (
                self.confidence_service.calculate_confidence(
                    comparison=comparison,
                    risk_result=risk_result,
                )
            )

            # --------------------------------------------------
            # RECOMMENDATION
            # --------------------------------------------------

            recommendation_result = (
                self.recommendation_service.recommend(
                    comparison=comparison,
                    risk_result=risk_result,
                    confidence_result=confidence_result,
                )
            )

            # --------------------------------------------------
            # COHERENCE
            # --------------------------------------------------

            coherence_result = (
                self.coherence_service.analyze_coherence(
                    old_version=old_version,
                    new_version=new_version,
                    comparison=comparison,
                )
            )

            # --------------------------------------------------
            # FILL REPORT
            # --------------------------------------------------

            report.summary = summary_result.get(
                "summary",
            )

            report.addition_count = summary_result.get(
                "addition_count",
                0,
            )

            report.deletion_count = summary_result.get(
                "deletion_count",
                0,
            )

            report.modification_count = summary_result.get(
                "modification_count",
                0,
            )

            report.important_changes = (
                summary_result.get(
                    "important_changes",
                    [],
                )
            )

            report.risks = risk_result.get(
                "risks",
                [],
            )

            report.confidence_score = (
                confidence_result.get(
                    "score",
                    0.0,
                )
            )

            report.confidence_level = (
                confidence_result.get(
                    "level",
                    "low",
                )
            )

            report.coherence_score = (
                coherence_result.get(
                    "score",
                    0.0,
                )
            )

            report.coherence_level = (
                coherence_result.get(
                    "level",
                    "critical",
                )
            )

            report.coherence_issues = (
                coherence_result.get(
                    "issues",
                    [],
                )
            )

            report.coherence_summary = (
                "The modification is coherent."
                if coherence_result.get(
                    "is_coherent",
                    True,
                )
                else
                "Potential coherence issues were detected."
            )

            report.recommendation = (
                recommendation_result.get(
                    "recommendation",
                    "verify",
                )
            )

            report.recommendation_reason = (
                recommendation_result.get(
                    "reason",
                )
            )

            db.add(report)
            db.commit()
            db.refresh(report)

            # --------------------------------------------------
            # COMPLETE AI ANALYSIS
            # --------------------------------------------------

            self.status_service.complete_analysis(
                db,
                report,
            )

            return report

        except Exception:

            # --------------------------------------------------
            # FAILED AI ANALYSIS
            # --------------------------------------------------

            self.status_service.fail_analysis(
                db,
                report,
            )

            raise