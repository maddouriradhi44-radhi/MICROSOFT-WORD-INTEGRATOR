from pathlib import Path

from app.word.parser import DocxParser


def test_parse_exported_section():

    file_path = Path(
        "storage/exports/test_section_export.docx"
    )

    parser = DocxParser()

    result = parser.parse(file_path)

    assert isinstance(result, dict)

    assert "title" in result
    assert "content" in result

    assert isinstance(result["title"], str)
    assert isinstance(result["content"], str)

    print("\nParsed title:", result["title"])
    print("\nParsed content:")
    print(result["content"])