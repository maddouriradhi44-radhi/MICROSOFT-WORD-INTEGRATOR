from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.document_status import DocumentStatus

class DocumentCreate(BaseModel):
    title: str
    project_id: int


class DocumentUpdate(BaseModel):
    title: str | None = None
    storage_key: str | None = None
    status: DocumentStatus | None = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    original_filename: str
    storage_key: str
    status: DocumentStatus
    owner_id: int
    project_id: int
    imported_at: datetime

    model_config = ConfigDict(from_attributes=True)