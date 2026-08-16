from pathlib import Path

from app.database.session import SessionLocal
from app.models.document_block import DocumentBlock
from app.word.exporter import DocxExporter


def test_export_docx():
    db = SessionLocal()

    try:
        blocks = (
            db.query(DocumentBlock)
            .order_by(DocumentBlock.id)
            .limit(10)
            .all()
        )

        assert blocks, "No document blocks found in database."

        original_path = Path(
            "app/tests/files/test_document.docx"
        )

        output_path = Path(
            "app/tests/files/exported_test.docx"
        )

        exporter = DocxExporter()

        result = exporter.export(
            original_path=original_path,
            output_path=output_path,
            blocks=blocks,
        )

        assert result.exists()
        assert result.stat().st_size > 0

    finally:
        db.close()