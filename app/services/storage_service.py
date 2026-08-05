"""
Storage service.

Handles document file storage.
"""

from pathlib import Path
import uuid
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class StorageService:
    """
    Manage uploaded files storage.
    """


    def __init__(self):

        self.storage_path = BASE_DIR / "storage" / "documents"


        # Create directory if not exists
        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
        )



    def save_file(
        self,
        file,
    ) -> str:
        """
        Save uploaded file and return storage key.

        The returned value is a relative path
        stored in the database.
        """


        extension = Path(
            file.filename
        ).suffix


        unique_name = (
            f"{uuid.uuid4()}{extension}"
        )


        absolute_path = (
            self.storage_path / unique_name
        )


        with open(
            absolute_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # Database value
        # Example:
        # storage/documents/file.docx

        storage_key = (
            Path("storage")
            / "documents"
            / unique_name
        )


        return storage_key.as_posix()



    def get_absolute_path(
        self,
        storage_key: str,
    ) -> Path:
        """
        Convert storage key into physical file path.

        Example:

        storage/documents/file.docx

        becomes:

        C:/Users/RADHI/Desktop/stage 2026/
        storage/documents/file.docx
        """


        return BASE_DIR / storage_key