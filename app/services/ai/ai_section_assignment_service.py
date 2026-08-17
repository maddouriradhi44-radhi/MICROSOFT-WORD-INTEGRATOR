"""
AI section assignment service.

Provides AI-based recommendations for assigning document
sections to suitable collaborator profiles.
"""

from __future__ import annotations


class AISectionAssignmentService:
    """
    Service responsible for recommending suitable collaborator
    profiles for document sections.
    """

    def recommend_role(
        self,
        title: str,
        content: str,
        keywords: list[str],
    ) -> dict:
        """
        Recommend a collaborator profile for a section.

        This is currently a rule-based foundation.
        The real AI model will be integrated later.
        """

        text = (
            f"{title} "
            f"{content} "
            f"{' '.join(keywords)}"
        ).lower()

        technical_keywords = [
            "api",
            "backend",
            "database",
            "sql",
            "postgresql",
            "fastapi",
            "python",
            "architecture",
            "server",
        ]

        testing_keywords = [
            "test",
            "testing",
            "qa",
            "validation",
            "quality",
        ]

        documentation_keywords = [
            "documentation",
            "guide",
            "manuel",
            "specification",
            "documentation technique",
        ]

        if any(
            keyword in text
            for keyword in technical_keywords
        ):
            role = "technical"

        elif any(
            keyword in text
            for keyword in testing_keywords
        ):
            role = "qa"

        elif any(
            keyword in text
            for keyword in documentation_keywords
        ):
            role = "documentation"

        else:
            role = "general"

        return {
            "recommended_role": role,
            "confidence": 0.70,
        }