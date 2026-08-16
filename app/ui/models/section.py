from dataclasses import dataclass
from typing import Any


@dataclass
class Section:
    id: int
    title: str
    content: str
    level: int
    order: int
    module: str
    status: str
    is_locked: bool
    document_id: int
    project_id: int
    assigned_user_id: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Section":
        return cls(
            id=data["id"],
            title=data.get("title", ""),
            content=data.get("content", ""),
            level=data.get("level", 0),
            order=data.get("order", 0),
            module=data.get("module", ""),
            status=data.get("status", ""),
            is_locked=data.get("is_locked", False),
            document_id=data["document_id"],
            project_id=data["project_id"],
            assigned_user_id=data.get("assigned_user_id"),
        )