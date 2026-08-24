"""
DOCX analyzer service.

This module analyzes Word documents and extracts:
- document sections
- document blocks
- original OOXML content
"""

from __future__ import annotations

from docx import Document
from docx.oxml.ns import qn


class DocxAnalyzerService:
    """
    Analyze DOCX documents and extract sections and document blocks.
    """

    def analyze(
        self,
        file_path: str,
    ) -> list[dict]:
        """
        Analyze a DOCX file.

        Returns:
            A list of detected sections containing document blocks.
        """

        document = Document(file_path)

        sections: list[dict] = []

        current_section: dict | None = None
        order_index = 0.0

        for element in document.element.body:

            # ==================================================
            # PARAGRAPH
            # ==================================================

            if element.tag == qn("w:p"):

                block_type = self._detect_paragraph_type(
                    element
                )

                text = self._get_paragraph_text(
                    element
                )

                # --------------------------------------------------
                # HEADING
                # --------------------------------------------------

                if block_type == "heading":

                    if current_section is not None:
                        sections.append(current_section)

                    level = self._get_heading_level(
                        element
                    )

                    current_section = {
                        "title": text,
                        "content": "",
                        "level": level,
                        "order": len(sections) + 1,
                        "blocks": [],
                    }

                    order_index = 0.0

                    current_section["blocks"].append(
                        {
                            "type": "heading",
                            "content_xml": element.xml,
                            "order_index": order_index,
                        }
                    )

                    order_index += 1.0

                    continue

                # --------------------------------------------------
                # CONTENT BEFORE FIRST HEADING
                # --------------------------------------------------

                if current_section is None:

                   current_section = {
                        "title": "Document Introduction",
                        "content": "",
                        "level": 1,
                        "order": len(sections) + 1,
                        "blocks": [],
                    }
                   order_index = 0.0

                # --------------------------------------------------
                # EMPTY PARAGRAPH
                # --------------------------------------------------

                if not text and block_type not in {
                    "image",
                    "page_break",
                }:
                    continue

                # --------------------------------------------------
                # ADD TEXT TO SECTION CONTENT
                # --------------------------------------------------

                if text:
                    if current_section["content"]:
                        current_section["content"] += "\n"

                    current_section["content"] += text

                # --------------------------------------------------
                # ADD BLOCK
                # --------------------------------------------------

                current_section["blocks"].append(
                    {
                        "type": block_type,
                        "content_xml": element.xml,
                        "order_index": order_index,
                    }
                )

                order_index += 1.0

            # ==================================================
            # TABLE
            # ==================================================

            elif element.tag == qn("w:tbl"):

                if current_section is None:

                    current_section = {
                        "title": "Document Introduction",
                        "content": "",
                        "level": 1,
                        "order": len(sections) + 1,
                        "blocks": [],
                    }

                    order_index = 0.0

                current_section["blocks"].append(
                    {
                        "type": "table",
                        "content_xml": element.xml,
                        "order_index": order_index,
                    }
                )

                order_index += 1.0

            # ==================================================
            # OTHER BODY ELEMENTS
            # ==================================================

            else:

                if current_section is None:

                    current_section = {
                        "title": "Document Introduction",
                        "content": "",
                        "level": 1,
                        "order": len(sections) + 1,
                        "blocks": [],
                    }
                    order_index = 0.0

                current_section["blocks"].append(
                    {
                        "type": self._detect_unknown_element_type(
                            element
                        ),
                        "content_xml": element.xml,
                        "order_index": order_index,
                    }
                )

                order_index += 1.0

        # ======================================================
        # SAVE LAST SECTION
        # ======================================================

        if current_section is not None:
            if (
                current_section["content"].strip()
                or current_section["blocks"]
            ):
                sections.append(current_section)

        return sections

    # ==========================================================
    # PARAGRAPH TYPE DETECTION
    # ==========================================================

    def _detect_paragraph_type(
        self,
        paragraph_element,
    ) -> str:

        # Heading
        p_pr = paragraph_element.find(
            qn("w:pPr")
        )

        if p_pr is not None:

            style_element = p_pr.find(
                qn("w:pStyle")
            )

            if style_element is not None:

                style_value = style_element.get(
                    qn("w:val")
                )

                if (
                    style_value is not None
                    and style_value.lower().startswith("heading")
                ):
                    return "heading"

        # Image
        if paragraph_element.find(
            ".//" + qn("a:blip")
        ) is not None:
            return "image"

        # Hyperlink
        if paragraph_element.find(
            ".//" + qn("w:hyperlink")
        ) is not None:
            return "hyperlink"

        # Page break
        for br in paragraph_element.iter(
            qn("w:br")
        ):
            if br.get(qn("w:type")) == "page":
                return "page_break"

        # List
        num_properties = paragraph_element.find(
            ".//" + qn("w:numPr")
        )

        if num_properties is not None:
            return "list"

        return "paragraph"

    # ==========================================================
    # TEXT EXTRACTION
    # ==========================================================

    def _get_paragraph_text(
        self,
        paragraph_element,
    ) -> str:

        texts = []

        for text_element in paragraph_element.iter(
            qn("w:t")
        ):
            if text_element.text:
                texts.append(
                    text_element.text
                )

        return "".join(texts).strip()

    # ==========================================================
    # HEADING LEVEL
    # ==========================================================

    def _get_heading_level(
        self,
        paragraph_element,
    ) -> int:

        p_pr = paragraph_element.find(
            qn("w:pPr")
        )

        if p_pr is None:
            return 1

        style_element = p_pr.find(
            qn("w:pStyle")
        )

        if style_element is None:
            return 1

        style_value = style_element.get(
            qn("w:val")
        )

        if not style_value:
            return 1

        style_value = style_value.lower()

        if style_value.startswith("heading"):

            suffix = style_value.replace(
                "heading",
                "",
                1,
            ).strip()

            try:
                return int(suffix)
            except ValueError:
                return 1

        return 1

    # ==========================================================
    # UNKNOWN ELEMENTS
    # ==========================================================

    def _detect_unknown_element_type(
        self,
        element,
    ) -> str:

        if element.tag == qn("w:sectPr"):
            return "section_break"

        return "unknown"