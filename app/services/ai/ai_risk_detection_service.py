"""
AI risk detection service.

Responsible for detecting potential risks
in modifications between two document versions.
"""

from __future__ import annotations
import re


class AIRiskDetectionService:
    """
    Service responsible for detecting risks
    in AI-detected version changes.
    """

    def detect_risks(
        self,
        comparison: dict,
    ) -> dict:
        """
        Detect potential risks in a version comparison.
        """

        risks = []

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

        # ==================================================
        # CONTRADICTION
        # ==================================================

        risks.extend(
            self._detect_contradictions(
                additions=additions,
                modifications=modifications,
            )
        )

        # ==================================================
        # IMPORTANT DELETIONS
        # ==================================================

        risks.extend(
            self._detect_important_deletions(
                deletions=deletions,
            )
        )

        # ==================================================
        # INCONSISTENCY
        # ==================================================

        risks.extend(
            self._detect_inconsistencies(
                additions=additions,
                modifications=modifications,
            )
        )

        # ==================================================
        # SUSPICIOUS CONTENT
        # ==================================================

        risks.extend(
            self._detect_suspicious_content(
                additions=additions,
                modifications=modifications,
            )
        )

        return {
            "has_risk": len(risks) > 0,
            "risks": risks,
        }

    # ==========================================================
    # TEXT EXTRACTION
    # ==========================================================

    @staticmethod
    def _extract_addition_texts(
        additions: list[dict],
    ) -> list[dict]:
        """
        Extract addition content while preserving location.
        """

        results = []

        for addition in additions:

            if not isinstance(
                addition,
                dict,
            ):
                continue

            content = addition.get(
                "content",
                [],
            )

            if isinstance(content, str):
                content = [content]

            for line in content:

                if isinstance(line, str):

                    results.append(
                        {
                            "text": line,
                            "new_start": addition.get(
                                "new_start"
                            ),
                            "new_end": addition.get(
                                "new_end"
                            ),
                        }
                    )

        return results

    @staticmethod
    def _extract_deletion_texts(
        deletions: list[dict],
    ) -> list[dict]:
        """
        Extract deletion content while preserving location.
        """

        results = []

        for deletion in deletions:

            if not isinstance(
                deletion,
                dict,
            ):
                continue

            content = deletion.get(
                "content",
                [],
            )

            if isinstance(content, str):
                content = [content]

            for line in content:

                if isinstance(line, str):

                    results.append(
                        {
                            "text": line,
                            "old_start": deletion.get(
                                "old_start"
                            ),
                            "old_end": deletion.get(
                                "old_end"
                            ),
                        }
                    )

        return results

    @staticmethod
    def _extract_modification_texts(
        modifications: list[dict],
    ) -> list[dict]:
        """
        Extract modification text while preserving
        old and new locations.
        """

        results = []

        for modification in modifications:

            if not isinstance(
                modification,
                dict,
            ):
                continue

            old_lines = modification.get(
                "old",
                [],
            )

            new_lines = modification.get(
                "new",
                [],
            )

            if isinstance(old_lines, str):
                old_lines = [old_lines]

            if isinstance(new_lines, str):
                new_lines = [new_lines]

            for line in old_lines:

                if isinstance(line, str):

                    results.append(
                        {
                            "text": line,
                            "side": "old",
                            "old_start": modification.get(
                                "old_start"
                            ),
                            "old_end": modification.get(
                                "old_end"
                            ),
                            "new_start": modification.get(
                                "new_start"
                            ),
                            "new_end": modification.get(
                                "new_end"
                            ),
                        }
                    )

            for line in new_lines:

                if isinstance(line, str):

                    results.append(
                        {
                            "text": line,
                            "side": "new",
                            "old_start": modification.get(
                                "old_start"
                            ),
                            "old_end": modification.get(
                                "old_end"
                            ),
                            "new_start": modification.get(
                                "new_start"
                            ),
                            "new_end": modification.get(
                                "new_end"
                            ),
                        }
                    )

        return results

    # ==========================================================
    # CONTRADICTION
    # ==========================================================

    def _detect_contradictions(
        self,
        additions: list[dict],
        modifications: list[dict],
    ) -> list[dict]:

        risks = []

        contradiction_pairs = [
            ("must", "must not"),
            ("should", "should not"),
            ("allowed", "forbidden"),
            ("enabled", "disabled"),
            ("active", "inactive"),
            ("required", "optional"),
            ("requires", "does not require"),
            ("require", "do not require"),
            ("true", "false"),
        ]

        texts = []

        texts.extend(
            self._extract_addition_texts(
                additions,
            )
        )

        texts.extend(
            self._extract_modification_texts(
                modifications,
            )
        )

        for positive, negative in contradiction_pairs:

            positive_pattern = rf"\b{positive}\b"

            negative_pattern = rf"\b{negative}\b"

            positive_items = []

            negative_items = []

            for item in texts:

                text = item["text"].lower()

                # For pairs such as:
                # must / must not
                # should / should not
                #
                # "must" must not match "must not".

                if positive in {"must", "should", "require", "requires"}:
                    has_positive = (
                        re.search(
                            rf"\b{positive}\b",
                            text,
                        ) is not None
                        and re.search(
                            rf"\b(?:do|does)\s+not\s+{positive}\b",
                            text,
                        ) is None
                    )
                else:
                    has_positive = (
                        re.search(
                            positive_pattern,
                            text,
                        ) is not None
                    )

                has_negative = (
                    re.search(
                        negative_pattern,
                        text,
                    )
                    is not None
                )

                if has_positive:
                    positive_items.append(item)

                if has_negative:
                    negative_items.append(item)

            if positive_items and negative_items:

                risks.append(
                    {
                        "type": "contradiction",
                        "severity": "critical",
                        "message": (
                            f"Potential contradiction detected "
                            f"between '{positive}' and "
                            f"'{negative}'."
                        ),
                        "locations": (
                            positive_items
                            + negative_items
                        ),
                    }
                )

        return risks

    # ==========================================================
    # IMPORTANT DELETIONS
    # ==========================================================

    def _detect_important_deletions(
        self,
        deletions: list[dict],
    ) -> list[dict]:

        risks = []

        important_terms = [
            "security",
            "authentication",
            "authorization",
            "password",
            "database",
            "api",
            "validation",
            "version",
            "backup",
            "permission",
            "project manager",
        ]

        deletion_items = (
            self._extract_deletion_texts(
                deletions,
            )
        )

        for item in deletion_items:

            text = item["text"]

            detected_terms = [
                term
                for term in important_terms
                if term in text.lower()
            ]

            if detected_terms:

                risks.append(
                    {
                        "type": "important_deletion",
                        "severity": "critical",
                        "message": (
                            "Important content may have "
                            "been removed."
                        ),
                        "terms": detected_terms,
                        "content": text,
                        "old_start": item["old_start"],
                        "old_end": item["old_end"],
                    }
                )

        return risks

    # ==========================================================
    # INCONSISTENCY
    # ==========================================================

    def _detect_inconsistencies(
        self,
        additions: list[dict],
        modifications: list[dict],
    ) -> list[dict]:

        risks = []

        texts = []

        texts.extend(
            self._extract_addition_texts(
                additions,
            )
        )

        texts.extend(
            self._extract_modification_texts(
                modifications,
            )
        )

        for item in texts:

            text = item["text"]
            normalized = text.lower()

            if (
                "fastapi" in normalized
                and "django" in normalized
            ):

                risks.append(
                    {
                        "type": "inconsistency",
                        "severity": "medium",
                        "message": (
                            "The modification mentions "
                            "different backend frameworks."
                        ),
                        "content": text,
                        "location": item,
                    }
                )

            if (
                "postgresql" in normalized
                and "mysql" in normalized
            ):

                risks.append(
                    {
                        "type": "inconsistency",
                        "severity": "medium",
                        "message": (
                            "The modification mentions "
                            "different database systems."
                        ),
                        "content": text,
                        "location": item,
                    }
                )

        return risks

    # ==========================================================
    # SUSPICIOUS CONTENT
    # ==========================================================

    def _detect_suspicious_content(
        self,
        additions: list[dict],
        modifications: list[dict],
    ) -> list[dict]:

        risks = []

        suspicious_terms = [
            "test reject",
            "test rejection",
            "modification test",
            "do not use",
            "temporary",
            "dummy",
            "fake",
            "xxx",
            "asdf",
            "qwerty",

            # French
            "refusée",
            "refusé",
            "refus",
            "à supprimer",
            "ne pas utiliser",
            "temporaire",
            "factice",
            "test de rejet",
            "modification sera refusée",

            # English
            "rejected",
            "reject",
            "do not accept",
        ]

        texts = []

        texts.extend(
            self._extract_addition_texts(
                additions,
            )
        )

        texts.extend(
            self._extract_modification_texts(
                modifications,
            )
        )

        for item in texts:

            text = item["text"]

            normalized = text.lower()

            detected_terms = [
                term
                for term in suspicious_terms
                if term in normalized
            ]

            if detected_terms:

                risks.append(
                    {
                        "type": "suspicious_content",
                        "severity": "medium",
                        "message": (
                            "Potentially suspicious "
                            "content was detected."
                        ),
                        "terms": detected_terms,
                        "content": text,
                        "location": item,
                    }
                )

        return risks