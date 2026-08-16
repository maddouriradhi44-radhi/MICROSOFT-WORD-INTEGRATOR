from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Notification:
    id: int
    user_id: int
    title: str
    message: str
    type: str
    level: str
    is_read: bool
    read_at: Optional[datetime]
    entity_type: Optional[str]
    entity_id: Optional[int]
    created_at: datetime

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            title=data["title"],
            message=data["message"],
            type=data["type"],
            level=data["level"],
            is_read=data["is_read"],
            read_at=(
                datetime.fromisoformat(data["read_at"])
                if data.get("read_at")
                else None
            ),
            entity_type=data.get("entity_type"),
            entity_id=data.get("entity_id"),
            created_at=datetime.fromisoformat(data["created_at"]),
        )