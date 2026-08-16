from pathlib import Path

from app.database.session import SessionLocal
from app.services.export_service import ExportService


def test_export_real_document():

    db = SessionLocal()

    try:
        service = ExportService()

        output_path = Path("storage/exports/test_export.docx")

        result = service.export_document(
            db=db,
            document_id=6,
            user_id=2,
            output_path=output_path,
        )

        assert result.exists()
        assert result.suffix == ".docx"
        assert result.stat().st_size > 0

        print("\nExported:", result)

    finally:
        db.close()


def test_export_real_section():

    db = SessionLocal()

    try:
        service = ExportService()

        output_path = Path(
            "storage/exports/test_section_export.docx"
        )

        result = service.export_section(
            db=db,
            section_id=14,
            user_id=2,
            output_path=output_path,
        )

        assert result.exists()
        assert result.suffix == ".docx"
        assert result.stat().st_size > 0

        print("\nSection exported:", result)

    finally:
        db.close()