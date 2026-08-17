"""
AI document classification service.

Responsible for classifying documents according to their
general logical and semantic nature.
"""

from __future__ import annotations

from app.schemas.ai import AIDocumentClassification


class AIClassificationService:
    """
    Service responsible for AI-based document classification.
    """

    def classify_document(
        self,
        sections: list[dict],
    ) -> AIDocumentClassification:
        """
        Classify a document based on its detected sections.

        Args:
            sections:
                Sections extracted from the DOCX document.

        Returns:
            AI-generated document classification.
        """

        if not sections:
            return AIDocumentClassification(
                document_type="unknown",
                language="unknown",
                confidence=0.0,
            )

        titles = [
            section.get("title", "")
            for section in sections
        ]

        contents = [
            section.get("content", "")
            for section in sections
        ]

        combined_text = " ".join(
            titles + contents
        ).lower()

        # ==================================================
        # LANGUAGE DETECTION
        # ==================================================

        french_keywords = [
            "le",
            "la",
            "les",
            "des",
            "une",
            "dans",
            "avec",
            "pour",
            "document",
            "projet",
            "système",
            "système",
            "section",
            "fonction",
            "utilisateur",
            "gestion",
        ]

        english_keywords = [
            "the",
            "a",
            "an",
            "of",
            "with",
            "for",
            "document",
            "project",
            "system",
            "section",
            "function",
            "user",
            "management",
        ]

        french_score = sum(
            1
            for keyword in french_keywords
            if f" {keyword} " in f" {combined_text} "
        )

        english_score = sum(
            1
            for keyword in english_keywords
            if f" {keyword} " in f" {combined_text} "
        )

        if french_score > english_score:
            language = "fr"

        elif english_score > french_score:
            language = "en"

        else:
            language = "unknown"

        # ==================================================
        # DOCUMENT TYPE
        # ==================================================

        if any(
            keyword in combined_text
            for keyword in [
                "requirement",
                "requirements",
                "functional requirements",
                "functional specification",
                "technical specification",
                "cahier des charges",
                "exigences",
                "spécification",
                "spécifications",
            ]
        ):
            document_type = "requirements_document"

        elif any(
            keyword in combined_text
            for keyword in [
                "architecture",
                "api",
                "backend",
                "database",
                "base de données",
                "technical",
                "technique",
                "software architecture",
            ]
        ):
            document_type = "technical_document"

        elif any(
            keyword in combined_text
            for keyword in [
                "contract",
                "contrat",
                "agreement",
                "accord",
            ]
        ):
            document_type = "contract"

        elif any(
            keyword in combined_text
            for keyword in [
                "report",
                "rapport",
                "analysis",
                "analyse",
            ]
        ):
            document_type = "report"

        elif any(
            keyword in combined_text
            for keyword in [
                "manual",
                "manuel",
                "user manual",
                "guide",
                "instructions",
            ]
        ):
            document_type = "user_manual"

        else:
            document_type = "general_document"

        return AIDocumentClassification(
            document_type=document_type,
            language=language,
            confidence=0.50,
        )