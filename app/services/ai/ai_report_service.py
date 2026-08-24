"""
AI report service.

This module orchestrates the complete AI analysis
of a modification between two document versions.
"""

from __future__ import annotations

from app.models.version import Version

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


class AIReportService:
    """
    Service responsible for generating the complete
    AI analysis report for a version modification.

    This service only analyzes and recommends.
    It does NOT approve or reject the modification.
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

    # ==========================================================
    # GENERATE REPORT
    # ==========================================================

    def generate_report(
        self,
        old_version: Version,
        new_version: Version,
    ) -> dict:
        """
        Generate the complete AI report for two versions.
        """

        # ------------------------------------------------------
        # 1. VERSION COMPARISON
        # ------------------------------------------------------

        comparison = (
            self.comparison_service.compare_versions(
                old_version=old_version,
                new_version=new_version,
            )
        )

        # ------------------------------------------------------
        # 2. CHANGE SUMMARY
        # ------------------------------------------------------

        summary = (
            self.summary_service.generate_summary(
                comparison=comparison,
            )
        )

        # ------------------------------------------------------
        # 3. RISK DETECTION
        # ------------------------------------------------------

        risk_result = (
            self.risk_service.detect_risks(
                comparison=comparison,
            )
        )

        # ------------------------------------------------------
        # 4. CONFIDENCE SCORE
        # ------------------------------------------------------

        confidence_result = (
            self.confidence_service.calculate_confidence(
                comparison=comparison,
                risk_result=risk_result,
            )
        )

        # ------------------------------------------------------
        # 5. RECOMMENDATION
        # ------------------------------------------------------

        recommendation = (
            self.recommendation_service.recommend(
                comparison=comparison,
                risk_result=risk_result,
                confidence_result=confidence_result,
            )
        )

        # ------------------------------------------------------
        # 6. COMPLETE REPORT
        # ------------------------------------------------------

        return {
            "section_id": new_version.section_id,

            "old_version": {
                "id": old_version.id,
                "version_number": old_version.version_number,
            },

            "new_version": {
                "id": new_version.id,
                "version_number": new_version.version_number,
            },

            "comparison": comparison,

            "summary": summary,

            "risks": risk_result,

            "confidence": confidence_result,

            "recommendation": recommendation,
        }