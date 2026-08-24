"""
AI document analyzer service.

Responsible for analyzing the complete logical structure
of a DOCX document and preparing an AI-based sectioning proposal.
"""

from __future__ import annotations

from app.schemas.ai import (
    AIDocumentProposal,
    AISectionProposal,
)

from app.services.ai.ai_section_analysis_service import (
    AISectionAnalysisService,
)


class AIDocumentAnalyzerService:
    """
    Service responsible for AI-based document analysis.

    The AI analyzes the complete document structure and
    proposes a logical decomposition into sections.

    IMPORTANT:
    This service only produces proposals.
    It does not create database Section records.
    """

    def __init__(self):
        self.section_analysis_service = (
            AISectionAnalysisService()
        )

    # ==========================================================
    # DOCUMENT ANALYSIS
    # ==========================================================

    def analyze_document(
        self,
        document_title: str,
        document_structure: list[dict],
    ) -> AIDocumentProposal:
        """
        Analyze a complete DOCX document.

        Existing DOCX sections are analyzed first.
        Detected subsections are promoted to independent
        section proposals.
        """

        sections: list[AISectionProposal] = []

        # ------------------------------------------------------
        # ANALYZE DOCUMENT STRUCTURE
        # ------------------------------------------------------

        for structure_item in document_structure:

            proposal = (
                self.section_analysis_service.analyze_section(
                    structure_item
                )
            )

            # --------------------------------------------------
            # If subsections exist, promote them to sections
            # --------------------------------------------------

            if proposal.subsections:

                # Parent section remains a valid proposal.
                sections.append(
                    proposal.model_copy(
                        update={
                            "subsections": [],
                        }
                    )
                )

                # Promote each subsection.
                for subsection in proposal.subsections:

                    sections.append(
                        AISectionProposal(
                            title=subsection.title,
                            level=subsection.level,
                            content=subsection.content,
                            order=len(sections) + 1,
                            reason=subsection.reason,
                            confidence=subsection.confidence,
                            category=subsection.category,
                            suggested_role=subsection.suggested_role,
                            keywords=subsection.keywords,
                            complexity=subsection.complexity,
                            subsections=[],
                        )
                    )

            else:

                sections.append(
                    proposal
                )

        # ------------------------------------------------------
        # Recalculate order
        # ------------------------------------------------------

        for index, section in enumerate(
            sections,
            start=1,
        ):
            sections[index - 1] = section.model_copy(
                update={
                    "order": index,
                }
            )

        # ------------------------------------------------------
        # Calculate document confidence
        # ------------------------------------------------------

        confidence = self._calculate_document_confidence(
            sections
        )

        return AIDocumentProposal(
            document_title=document_title,
            sections=sections,
            reason=(
                "The document was analyzed according to "
                "its structure, content, hierarchy and "
                "logical organization."
            ),
            confidence=confidence,
        )

    # ==========================================================
    # DOCUMENT CONFIDENCE
    # ==========================================================

    def _calculate_document_confidence(
        self,
        sections: list[AISectionProposal],
    ) -> float:
        """
        Calculate an overall confidence score for the
        document decomposition proposal.
        """

        if not sections:
            return 0.0

        total = sum(
            section.confidence
            for section in sections
        )

        return min(
            total / len(sections),
            1.0,
        )