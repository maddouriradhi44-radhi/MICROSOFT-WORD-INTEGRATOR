from docx import Document


class DocxAnalyzerService:


    def analyze(
        self,
        file_path: str,
    ):

        document = Document(file_path)


        sections = []

        current_section = None


        for paragraph in document.paragraphs:


            text = paragraph.text.strip()


            if not text:
                continue



            # Detect Word heading styles
            if paragraph.style.name.startswith("Heading"):


                if current_section:
                    sections.append(
                        current_section
                    )


                current_section = {
                    "title": text,
                    "content": ""
                }



            else:

                # Add paragraph text to the current section
                if current_section:

                    current_section["content"] += (
                        text + "\n"
                    )



        # Save the last extracted section
        if current_section:
            sections.append(
                current_section
            )


        return sections