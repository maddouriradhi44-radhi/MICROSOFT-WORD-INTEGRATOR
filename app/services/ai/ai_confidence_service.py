"""
AI confidence score service.

Responsible for calculating a confidence score
for the analysis of a document version modification.
"""

from __future__ import annotations


class AIConfidenceService:
    """
    Service responsible for calculating
    the confidence level of an AI analysis.
    """

    def calculate_confidence(
        self,
        comparison: dict,
        risk_result: dict,
    ) -> dict:
        """
        Calculate a confidence score based on:

        - detected changes
        - detected risks
        - amount of modifications
        """

        score = 1.0

        additions = comparison.get(
            "additions",
            [],
        )

        deletions = comparison.get(
            "deletions",
            [],
        )

        modifications = comparison.get(
            "modifications",
            [],
        )

        risks = risk_result.get(
            "risks",
            [],
        )

        # ==================================================
        # NO CHANGE
        # ==================================================

        if not (
            additions
            or deletions
            or modifications
        ):
            return {
                "score": 1.0,
                "level": "high",
            }

        # ==================================================
        # CHANGES
        # ==================================================

        total_changes = (
            len(additions)
            + len(deletions)
            + len(modifications)
        )

        # More changes => lower confidence
        if total_changes >= 10:
            score -= 0.30

        elif total_changes >= 5:
            score -= 0.15

        elif total_changes >= 2:
            score -= 0.05

        # ==================================================
        # RISKS
        # ==================================================

        for risk in risks:

            severity = risk.get(
                "severity",
                "medium",
            )

            if severity == "critical":
                score -= 0.20

            elif severity == "medium":
                score -= 0.10

            elif severity == "low":
                score -= 0.05
        # ==================================================
        # LIMIT SCORE
        # ==================================================

        score = max(
            0.0,
            min(score, 1.0),
        )

        # ==================================================
        # LEVEL
        # ==================================================

        if score < 0.40:
            level = "critical"

        elif score < 0.70:
            level = "medium"

        else:
            level = "high"

        return {
            "score": round(
                score,
                2,
            ),
            "level": level,
        }