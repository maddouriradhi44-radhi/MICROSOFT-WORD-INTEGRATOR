from pathlib import Path

from app.database.session import SessionLocal
from app.services.import_service import ImportService


class TestUploadFile:
    def __init__(self, path: str):
        self.path = Path(path)
        self.filename = self.path.name
        self.file = open(self.path, "rb")

    def close(self):
        self.file.close()


db = SessionLocal()

file = TestUploadFile(
    "storage/exports/test_ai_section_16_modified.docx"
)

try:
    service = ImportService()

    print()
    print("===== AI IMPORT WORKFLOW TEST =====")
    print()

    result = service.import_section(
        db=db,
        section_id=16,
        user_id=3,
        file=file,
    )

    print()
    print("===== IMPORT RESULT =====")
    print()

    for key, value in result.items():
        print(f"{key}: {value}")

finally:
    file.close()
    db.close()