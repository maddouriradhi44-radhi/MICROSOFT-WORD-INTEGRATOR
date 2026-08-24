"""
AI validation decision service.

Determines whether a version can be automatically
validated by AI or requires Project Manager review.
"""

from __future__ import annotations

from app.models.ai_validation_report import AIValidationReport


class AIValidationDecisionService:
    """
    Determines whether an AI validation report allows
    automatic validation.

    The AI only determines whether automatic validation
    is safe according to predefined rules.

    The Project Manager remains responsible for the
    final human decision whenever manual review is required.
    """

    # ==========================================================
    # AUTO VALIDATION THRESHOLDS
    # ==========================================================

    MIN_CONFIDENCE_SCORE = 0.70
    MIN_COHERENCE_SCORE = 0.70

    # ==========================================================
    # AUTO VALIDATION DECISION
    # ==========================================================

    @classmethod
    def can_auto_validate(
        cls,
        report: AIValidationReport,
    ) -> bool:
        """
        Return True only when the AI analysis is sufficiently
        reliable for automatic validation.

        Automatic validation requires all of the following:

        - no medium, high, or critical risk;
        - high confidence;
        - confidence score >= 0.70;
        - high coherence;
        - coherence score >= 0.70;
        - recommendation == "accept".

        Otherwise, the version must be reviewed by the
        Project Manager.

        The AI never performs a definitive rejection.
        """

        # ======================================================
        # 1. RISKS
        # ======================================================

        risks = report.risks or []

        has_blocking_risk = any(
            isinstance(risk, dict)
            and risk.get("severity") in {
                "medium",
                "high",
                "critical",
            }
            for risk in risks
        )

        if has_blocking_risk:
            return False

        # ======================================================
        # 2. CONFIDENCE
        # ======================================================

        confidence_score = report.confidence_score or 0.0
        confidence_level = (
            report.confidence_level or ""
        ).lower()

        if confidence_score < cls.MIN_CONFIDENCE_SCORE:
            return False

        if confidence_level != "high":
            return False

        # ======================================================
        # 3. COHERENCE
        # ======================================================

        coherence_score = report.coherence_score or 0.0
        coherence_level = (
            report.coherence_level or ""
        ).lower()

        if coherence_score < cls.MIN_COHERENCE_SCORE:
            return False

        if coherence_level != "high":
            return False

        # ======================================================
        # 4. AI RECOMMENDATION
        # ======================================================

        recommendation = (
            report.recommendation or ""
        ).lower()

        if recommendation != "accept":
            return False

        # ======================================================
        # 5. SAFE FOR AUTOMATIC VALIDATION
        # ======================================================

        return True