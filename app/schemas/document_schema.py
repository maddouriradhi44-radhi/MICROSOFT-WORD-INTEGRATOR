from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.document_status import DocumentStatus

class DocumentCreate(BaseModel):
    title: str
    file_path: str
    project_id: int

class DocumentUpdate(BaseModel):
    title: str | None = None
    file_path: str | None = None
    status: DocumentStatus | None = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_path: str
    status: DocumentStatus
    owner_id: int
    project_id: int
    imported_at: datetime

    model_config = ConfigDict(from_attributes=True)