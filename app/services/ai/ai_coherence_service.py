"""
AI coherence analysis service.

Responsible for detecting potential coherence issues
between two versions of a document section.
"""

from __future__ import annotations

import re

from app.models.version import Version


class AICoherenceService:
    """
    Service responsible for analyzing the coherence
    between an old and a new section version.

    This service only analyzes the modification.
    It does not approve or reject the validation.
    """

    # ==========================================================
    # ANALYZE COHERENCE
    # ==========================================================

    def analyze_coherence(
        self,
        old_version: Version,
        new_version: Version,
        comparison: dict,
    ) -> dict:
        """
        Analyze the coherence of a modification.

        Returns:
            A structured coherence result containing:
            - is_coherent
            - score
            - level
            - issues
        """

        issues = []

        old_content = (
            old_version.content_snapshot or ""
        )

        new_content = (
            new_version.content_snapshot or ""
        )

        # ======================================================
        # 1. FRAMEWORK / TECHNOLOGY CONFLICTS
        # ======================================================

        issues.extend(
            self._detect_technology_conflicts(
                new_content,
            )
        )

        # ======================================================
        # 2. CONTRADICTIONS
        # ======================================================

        issues.extend(
            self._detect_contradictions(
                old_content=old_content,
                new_content=new_content,
            )
        )

        # ======================================================
        # 3. NUMBER / VALUE INCONSISTENCIES
        # ======================================================

        issues.extend(
            self._detect_value_inconsistencies(
                old_content=old_content,
                new_content=new_content,
            )
        )

        # ======================================================
        # 4. CALCULATE SCORE
        # ======================================================

        score = self._calculate_score(
            issues=issues,
            comparison=comparison,
        )

        # ======================================================
        # 5. LEVEL
        # ======================================================

        level = self._get_level(score)

        # ======================================================
        # 6. COHERENCE
        # ======================================================

        is_coherent = not any(
            issue.get("severity") == "high"
            for issue in issues
        )

        return {
            "is_coherent": is_coherent,
            "score": score,
            "level": level,
            "issues": issues,
        }

    # ==========================================================
    # TECHNOLOGY CONFLICTS
    # ==========================================================

    def _detect_technology_conflicts(
        self,
        content: str,
    ) -> list[dict]:
        """
        Detect potentially conflicting technologies
        mentioned in the same version.
        """

        issues = []

        technology_groups = [
            {
                "name": "backend_framework",
                "technologies": [
                    "fastapi",
                    "django",
                    "flask",
                    "spring boot",
                ],
            },
            {
                "name": "database",
                "technologies": [
                    "postgresql",
                    "mysql",
                    "mongodb",
                    "sqlite",
                ],
            },
            {
                "name": "frontend_framework",
                "technologies": [
                    "react",
                    "angular",
                    "vue",
                ],
            },
        ]

        normalized = content.lower()

        for group in technology_groups:

            detected = [
                technology
                for technology in group["technologies"]
                if technology in normalized
            ]

            if len(detected) > 1:

                issues.append(
                    {
                        "type": "technology_conflict",
                        "severity": "medium",
                        "category": group["name"],
                        "technologies": detected,
                        "message": (
                            "Multiple technologies from the same "
                            "category were detected: "
                            + ", ".join(detected)
                            + "."
                        ),
                    }
                )

        return issues

    # ==========================================================
    # CONTRADICTIONS
    # ==========================================================

    def _detect_contradictions(
        self,
        old_content: str,
        new_content: str,
    ) -> list[dict]:
        """
        Detect simple semantic contradictions introduced
        by the new version.
        """

        issues = []

        old_normalized = old_content.lower()
        new_normalized = new_content.lower()

        contradiction_pairs = [
            ("must", "must not"),
            ("should", "should not"),
            ("allowed", "forbidden"),
            ("enabled", "disabled"),
            ("active", "inactive"),
            ("required", "optional"),
            ("true", "false"),
        ]

        for positive, negative in contradiction_pairs:

            old_has_positive = (
                positive in old_normalized
            )

            old_has_negative = (
                negative in old_normalized
            )

            new_has_positive = (
                positive in new_normalized
            )

            new_has_negative = (
                negative in new_normalized
            )

            # --------------------------------------------------
            # Contradiction introduced by the new version
            # --------------------------------------------------

            if (
                new_has_positive
                and new_has_negative
                and not (
                    old_has_positive
                    and old_has_negative
                )
            ):

                issues.append(
                    {
                        "type": "contradiction",
                        "severity": "high",
                        "terms": [
                            positive,
                            negative,
                        ],
                        "message": (
                            "The new version contains potentially "
                            "contradictory statements involving "
                            f"'{positive}' and '{negative}'."
                        ),
                    }
                )

        return issues

    # ==========================================================
    # VALUE INCONSISTENCIES
    # ==========================================================

    def _detect_value_inconsistencies(
        self,
        old_content: str,
        new_content: str,
    ) -> list[dict]:
        """
        Detect simple numerical inconsistencies.

        This is intentionally conservative and only reports
        potentially relevant numeric changes.
        """

        issues = []

        old_numbers = set(
            re.findall(
                r"\b\d+(?:\.\d+)?\b",
                old_content,
            )
        )

        new_numbers = set(
            re.findall(
                r"\b\d+(?:\.\d+)?\b",
                new_content,
            )
        )

        removed_numbers = old_numbers - new_numbers
        added_numbers = new_numbers - old_numbers

        if removed_numbers and added_numbers:

            issues.append(
                {
                    "type": "value_change",
                    "severity": "low",
                    "old_values": sorted(
                        removed_numbers,
                    ),
                    "new_values": sorted(
                        added_numbers,
                    ),
                    "message": (
                        "Numerical values changed between "
                        "the two versions. The Project Manager "
                        "should verify that the new values "
                        "are intentional."
                    ),
                }
            )

        return issues

    # ==========================================================
    # SCORE
    # ==========================================================

    def _calculate_score(
        self,
        issues: list[dict],
        comparison: dict,
    ) -> float:
        """
        Calculate a coherence score between 0 and 1.
        """

        score = 1.0

        for issue in issues:

            severity = issue.get(
                "severity",
                "low",
            )

            if severity == "high":
                score -= 0.35

            elif severity == "medium":
                score -= 0.15

            elif severity == "low":
                score -= 0.05

        # --------------------------------------------------
        # Large modifications slightly reduce confidence
        # --------------------------------------------------

        total_changes = (
            len(comparison.get("additions", []))
            + len(comparison.get("deletions", []))
            + len(comparison.get("modifications", []))
        )

        if total_changes >= 10:
            score -= 0.10

        elif total_changes >= 5:
            score -= 0.05

        score = max(
            0.0,
            min(score, 1.0),
        )

        return round(
            score,
            2,
        )

    # ==========================================================
    # LEVEL
    # ==========================================================

    def _get_level(
        self,
        score: float,
    ) -> str:
        """
        Convert a coherence score into a level.
        """

        if score < 0.40:
            return "critical"

        if score < 0.70:
            return "medium"

        return "high"
