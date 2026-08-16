"""
DOCX parser.

Parses a DOCX file imported after external editing
in Microsoft Word.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document


class DocxParser:
    """
    Parse a DOCX file and extract its textual content.
    """

    def parse(
        self,
        file_path: str | Path,
        expected_title: str | None = None,
    ) -> dict:
        """
        Parse a DOCX file.

        Args:
            file_path:
                Path to the DOCX file.

            expected_title:
                Current title of the section in the platform.
                When provided, the parser uses it to determine
                whether the first paragraph is actually a title.

        Returns:
            A dictionary containing:
            - title
            - content
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"DOCX file not found: {file_path}"
            )

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        # ==================================================
        # TITLE / CONTENT
        # ==================================================

        title = expected_title or ""

        content_paragraphs = paragraphs

        # --------------------------------------------------
        # If the first paragraph matches the expected title,
        # it is a real title and must not remain in content.
        # --------------------------------------------------

        if (
            expected_title
            and paragraphs
            and paragraphs[0].strip()
            == expected_title.strip()
        ):
            content_paragraphs = paragraphs[1:]

        # --------------------------------------------------
        # Legacy behavior when no expected title is supplied
        # --------------------------------------------------

        elif expected_title is None and paragraphs:

            title = paragraphs[0]
            content_paragraphs = paragraphs

        content = "\n".join(
            content_paragraphs
        )

        return {
            "title": title,
            "content": content,
        }