from app.services.docx_analyzer_service import DocxAnalyzerService


def test_docx_analyzer_service():
    analyzer = DocxAnalyzerService()

    sections = analyzer.analyze(
        "app/tests/files/test_document.docx"
    )

    assert sections

    for section in sections:

        assert "title" in section
        assert "level" in section
        assert "blocks" in section

        assert section["blocks"]

        for block in section["blocks"]:

            assert "type" in block
            assert "content_xml" in block
            assert "order_index" in block

            assert block["content_xml"]