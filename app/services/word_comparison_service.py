"""
Word comparison service.

Compares the current section content with content
parsed from a DOCX file edited externally.
"""

from __future__ import annotations


class WordComparisonService:
    """
    Compare the current section with an externally edited DOCX.
    """

    def compare(
        self,
        current_title: str,
        current_content: str,
        imported_title: str,
        imported_content: str,
    ) -> dict:
        """
        Compare current section data with imported DOCX data.

        Returns:
            A dictionary describing the detected changes.
        """

        title_changed = (
            current_title.strip()
            != imported_title.strip()
        )

        content_changed = (
            current_content.strip()
            != imported_content.strip()
        )

        return {
            "changed": (
                title_changed
                or content_changed
            ),
            "title_changed": title_changed,
            "content_changed": content_changed,
            "current_title": current_title,
            "imported_title": imported_title,
            "current_content": current_content,
            "imported_content": imported_content,
        }