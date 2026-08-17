"""
AI section analysis service.

Responsible for analyzing an individual document section
and preparing an AI-based analysis proposal.
"""

from __future__ import annotations

from app.schemas.ai import AISectionProposal


class AISectionAnalysisService:
    """
    Service responsible for AI-based section analysis.
    """

    def analyze_section(
        self,
        section: dict,
    ) -> AISectionProposal:
        """
        Analyze a single document section.

        Args:
            section: Section extracted from the DOCX analyzer.

        Returns:
            AISectionProposal containing the analysis proposal.
        """

        title = section.get("title", "")
        content = section.get("content", "")
        level = section.get("level", 1)

        keywords = self._extract_keywords(
            title=title,
            content=content,
        )

        suggested_role = self._suggest_role(
            title=title,
            content=content,
        )

        complexity = self._estimate_complexity(
            content=content,
        )

        confidence = self._calculate_confidence(
            title=title,
            content=content,
            level=level,
        )

        reason = (
            "The section was analyzed according to "
            "its title, content, structure and complexity."
        )

        return AISectionProposal(
            title=title,
            level=level,
            content=content,
            reason=reason,
            confidence=confidence,
            suggested_role=suggested_role,
            keywords=keywords,
            complexity=complexity,
        )

    # ==========================================================
    # KEYWORDS
    # ==========================================================

    def _extract_keywords(
        self,
        title: str,
        content: str,
    ) -> list[str]:

        text = f"{title} {content}".lower()

        technical_keywords = [
            "api",
            "backend",
            "frontend",
            "fastapi",
            "python",
            "database",
            "postgresql",
            "sql",
            "architecture",
            "security",
            "authentication",
            "software",
            "application",
        ]

        detected = []

        for keyword in technical_keywords:
            if keyword in text:
                detected.append(keyword)

        return detected

    # ==========================================================
    # ROLE SUGGESTION
    # ==========================================================

    def _suggest_role(
        self,
        title: str,
        content: str,
    ) -> str | None:

        text = f"{title} {content}".lower()

        technical_terms = [
            "api",
            "backend",
            "frontend",
            "database",
            "architecture",
            "python",
            "fastapi",
            "sql",
            "security",
            "authentication",
        ]

        if any(term in text for term in technical_terms):
            return "technical"

        if any(
            term in text
            for term in [
                "test",
                "testing",
                "validation",
                "quality",
            ]
        ):
            return "qa"

        if any(
            term in text
            for term in [
                "management",
                "project",
                "planning",
                "budget",
            ]
        ):
            return "management"

        return "general"

    # ==========================================================
    # COMPLEXITY
    # ==========================================================

    def _estimate_complexity(
        self,
        content: str,
    ) -> str:

        word_count = len(
            content.split()
        )

        if word_count < 100:
            return "low"

        if word_count < 300:
            return "medium"

        return "high"

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    def _calculate_confidence(
        self,
        title: str,
        content: str,
        level: int,
    ) -> float:

        confidence = 0.5

        if title.strip():
            confidence += 0.2

        if content.strip():
            confidence += 0.2

        if level >= 1:
            confidence += 0.1

        return min(
            confidence,
            1.0,
        )