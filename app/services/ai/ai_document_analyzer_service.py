"""
AI document analyzer service.

Responsible for analyzing the logical structure of a DOCX
document and preparing an AI-based sectioning proposal.
"""

from __future__ import annotations

from app.schemas.ai import AISectionProposal


class AIDocumentAnalyzerService:
    """
    Service responsible for AI-based document analysis.
    """

    def analyze_document(
        self,
        sections: list[dict],
    ) -> list[AISectionProposal]:
        """
        Analyze the detected document sections.

        Args:
            sections: Sections extracted by DocxAnalyzerService.

        Returns:
            A list of AI section proposals.
        """

        proposals: list[AISectionProposal] = []

        for section in sections:

            title = section.get(
                "title",
                "",
            )

            content = section.get(
                "content",
                "",
            )

            combined_text = (
                f"{title} {content}"
            ).lower()

            suggested_role = (
                self._suggest_role(
                    combined_text
                )
            )

            keywords = (
                self._extract_keywords(
                    combined_text
                )
            )

            complexity = (
                self._estimate_complexity(
                    content
                )
            )

            proposal = AISectionProposal(
                title=title,
                level=section.get(
                    "level",
                    1,
                ),
                content=content,
                reason=(
                    "Section analyzed from its title "
                    "and content."
                ),
                confidence=self._estimate_confidence(
                    suggested_role=suggested_role,
                    keywords=keywords,
                ),
                suggested_role=suggested_role,
                keywords=keywords,
                complexity=complexity,
            )

            proposals.append(proposal)

        return proposals

    # ==========================================================
    # ROLE SUGGESTION
    # ==========================================================

    def _suggest_role(
        self,
        text: str,
    ) -> str | None:
        """
        Suggest a project role according to the section content.
        """

        if any(
            keyword in text
            for keyword in [
                "architecture",
                "backend",
                "api",
                "database",
                "base de données",
                "technical",
                "technique",
                "software",
            ]
        ):
            return "technical"

        if any(
            keyword in text
            for keyword in [
                "requirement",
                "requirements",
                "fonctionnalité",
                "fonctionnalités",
                "exigence",
                "exigences",
                "cahier des charges",
            ]
        ):
            return "functional"

        if any(
            keyword in text
            for keyword in [
                "test",
                "testing",
                "validation",
                "quality",
                "qualité",
            ]
        ):
            return "qa"

        if any(
            keyword in text
            for keyword in [
                "management",
                "gestion",
                "planning",
                "project management",
                "gestion de projet",
                "milestone",
                "milestones",
                "ressource",
                "ressources",
                "schedule",
                "planning projet",
            ]
        ):
            return "management"

        return None

    # ==========================================================
    # KEYWORDS
    # ==========================================================

    def _extract_keywords(
        self,
        text: str,
    ) -> list[str]:
        """
        Extract a small set of meaningful keywords.
        """

        known_keywords = [
            "architecture",
            "api",
            "backend",
            "database",
            "base de données",
            "requirement",
            "requirements",
            "fonctionnalité",
            "exigence",
            "test",
            "testing",
            "validation",
            "quality",
            "qualité",
            "management",
            "gestion",
            "planning",
            "project management",
            "gestion de projet",
            "milestone",
            "milestones",
            "ressource",
            "ressources",
            "schedule",
        ]

        return [
            keyword
            for keyword in known_keywords
            if keyword in text
        ]

    # ==========================================================
    # COMPLEXITY
    # ==========================================================

    def _estimate_complexity(
        self,
        content: str,
    ) -> str:
        """
        Estimate section complexity based on content size.

        This is only a baseline before integration
        with a real AI model.
        """

        word_count = len(
            content.split()
        )

        if word_count < 50:
            return "low"

        if word_count < 150:
            return "medium"

        return "high"

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    def _estimate_confidence(
        self,
        suggested_role: str | None,
        keywords: list[str],
    ) -> float:
        """
        Estimate the confidence of the section analysis.

        This is a deterministic baseline before integration
        with a real AI model.
        """

        if suggested_role is None:
            return 0.30

        keyword_count = len(keywords)

        if keyword_count >= 3:
            return 0.90

        if keyword_count == 2:
            return 0.75

        if keyword_count == 1:
            return 0.60

        return 0.40