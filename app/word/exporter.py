"""
DOCX exporter.

Reconstructs a Word document from stored document blocks
while preserving the original DOCX package.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree


WORD_NAMESPACE = (
    "http://schemas.openxmlformats.org/"
    "wordprocessingml/2006/main"
)

NS = {
    "w": WORD_NAMESPACE,
}


class DocxExporter:
    """
    Reconstruct a DOCX document from stored OOXML blocks.
    """

    def export(
        self,
        original_path: str | Path,
        output_path: str | Path,
        blocks: list,
    ) -> Path:
        """
        Create a new DOCX file from the original document package
        and the selected document blocks.

        Only the supplied document blocks are inserted into the
        document body. The original section properties (w:sectPr)
        are preserved as the final body element.
        """

        original_path = Path(original_path)
        output_path = Path(output_path)

        if not original_path.exists():
            raise FileNotFoundError(
                f"Original DOCX not found: {original_path}"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with ZipFile(
            original_path,
            "r",
        ) as source_zip:

            document_xml = source_zip.read(
                "word/document.xml"
            )

            document_tree = etree.fromstring(
                document_xml
            )

            body = document_tree.find(
                "w:body",
                NS,
            )

            if body is None:
                raise ValueError(
                    "Invalid DOCX: document body not found."
                )

            # --------------------------------------------------
            # Preserve the original section properties.
            # --------------------------------------------------

            sect_pr = body.find(
                "w:sectPr",
                NS,
            )

            preserved_sect_pr = (
                deepcopy(sect_pr)
                if sect_pr is not None
                else None
            )

            # --------------------------------------------------
            # Remove every existing body child.
            # --------------------------------------------------

            for child in list(body):
                body.remove(child)

            # --------------------------------------------------
            # Add only the stored blocks.
            # --------------------------------------------------

            ordered_blocks = sorted(
                blocks,
                key=lambda block: block.order_index,
            )

            for block in ordered_blocks:

                if not block.content_xml:
                    continue

                try:
                    element = etree.fromstring(
                        block.content_xml.encode("utf-8")
                    )
                except (
                    etree.XMLSyntaxError,
                    ValueError,
                ) as exc:
                    raise ValueError(
                        f"Invalid OOXML for block {block.id}"
                    ) from exc

                body.append(
                    deepcopy(element)
                )

            # --------------------------------------------------
            # w:sectPr MUST remain the last body element.
            # --------------------------------------------------

            if preserved_sect_pr is not None:
                body.append(
                    preserved_sect_pr
                )

            new_document_xml = etree.tostring(
                document_tree,
                xml_declaration=True,
                encoding="UTF-8",
                standalone="yes",
            )

            # --------------------------------------------------
            # Rebuild DOCX package.
            # --------------------------------------------------

            with ZipFile(
                output_path,
                "w",
                ZIP_DEFLATED,
            ) as destination_zip:

                for item in source_zip.infolist():

                    if item.filename == "word/document.xml":

                        destination_zip.writestr(
                            item,
                            new_document_xml,
                        )

                    else:

                        destination_zip.writestr(
                            item,
                            source_zip.read(
                                item.filename
                            ),
                        )

        return output_path