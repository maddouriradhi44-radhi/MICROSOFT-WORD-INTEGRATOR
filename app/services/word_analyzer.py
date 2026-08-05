"""
Word document analyzer service.

This module analyzes a .docx file
and extracts sections and blocks.
"""

from docx import Document


class WordAnalyzer:
    """
    Analyze Word documents and extract structure.
    """


    def analyze(self, file_path: str):
        """
        Analyze a Word document.

        Returns detected sections with their blocks.
        """

        document = Document(file_path)

        sections = []

        current_section = None


        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if not text:
                continue


            style = paragraph.style.name

            # Heading detected
            if style.startswith("Heading"):

                level = int(
                    style.replace("Heading ", "")
                )


                current_section = {
                    "title": text,
                    "level": level,
                    "blocks": []
                }


                sections.append(current_section)


            else:

                # Paragraph inside current section
                if current_section:

                    current_section["blocks"].append(
                        {
                            "type": "paragraph",
                            "content": text
                        }
                    )


        return sections