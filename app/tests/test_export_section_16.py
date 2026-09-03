from pathlib import Path

from app.database.session import SessionLocal
from app.services.export_service import ExportService


db = SessionLocal()

try:
    service = ExportService()

    output_path = Path(
        "storage/exports/test_ai_section_16.docx"
    )

    result = service.export_section(
        db=db,
        section_id=16,
        user_id=3,
        output_path=output_path,
    )

    print()
    print("===== EXPORT TEST =====")
    print()
    print("Exported:", result)
    print("Exists:", result.exists())
    print("Size:", result.stat().st_size)
    print()

finally:
    db.close()