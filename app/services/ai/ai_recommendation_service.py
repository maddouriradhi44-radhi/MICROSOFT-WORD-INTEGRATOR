"""
AI recommendation service.

Responsible for generating a recommendation
for the Project Manager based on AI analysis.
"""

from __future__ import annotations


class AIRecommendationService:
    """
    Service responsible for generating an AI recommendation.

    The recommendation is only a suggestion.
    It does not approve or reject the version.
    """

    def recommend(
        self,
        comparison: dict,
        risk_result: dict,
        confidence_result: dict,
    ) -> dict:
        """
        Generate a recommendation for the Project Manager.

        Possible recommendations:

        - accept
        - verify
        - reject
        """

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

        score = confidence_result.get(
            "score",
            0.0,
        )

        # ==================================================
        # NO CHANGES
        # ==================================================

        if not (
            additions
            or deletions
            or modifications
        ):
            return {
                "recommendation": "accept",
                "reason": (
                    "No significant modification "
                    "was detected."
                ),
            }

        # ==================================================
        # HIGH RISKS
        # ==================================================

        critical_risks = [
            risk
            for risk in risks
            if isinstance(risk, dict)
            and risk.get("severity") == "critical"
        ]

        if critical_risks:
            return {
                "recommendation": "reject",
                "reason": (
                    "High-risk changes were detected. "
                    "The Project Manager should review "
                    "the modification carefully."
                ),
            }

        # ==================================================
        # LOW CONFIDENCE
        # ==================================================

        if score < 0.40:
            return {
                "recommendation": "reject",
                "reason": (
                    "The AI confidence score is critical. "
                    "The modification requires manual review "
                    "before acceptance."
                ),
            }

        # ==================================================
        # MEDIUM RISKS
        # ==================================================

        if risks:
            return {
                "recommendation": "verify",
                "reason": (
                    "Potential risks were detected. "
                    "The Project Manager should verify "
                    "the modification before accepting it."
                ),
            }

        # ==================================================
        # SIGNIFICANT MODIFICATIONS
        # ==================================================

        total_changes = (
            len(additions)
            + len(deletions)
            + len(modifications)
        )

        if total_changes >= 5:
            return {
                "recommendation": "verify",
                "reason": (
                    "Several changes were detected. "
                    "The Project Manager should verify "
                    "the modification."
                ),
            }

        # ==================================================
        # DEFAULT
        # ==================================================

        return {
            "recommendation": "accept",
            "reason": (
                "The modification contains no significant "
                "risk according to the AI analysis."
            ),
        }