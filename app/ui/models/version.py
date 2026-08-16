from dataclasses import dataclass
from datetime import datetime


@dataclass
class Version:
    id: int
    version_number: int
    title_snapshot: str
    content_snapshot: str
    change_comment: str | None
    is_current: bool
    is_archived: bool
    section_id: int
    author_id: int
    created_at: datetime
    change_type: str

    @classmethod
    def from_dict(cls, data: dict) -> "Version":
        created_at = data.get("created_at")

        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(
                created_at.replace("Z", "+00:00")
            )

        return cls(
            id=data["id"],
            version_number=data["version_number"],
            title_snapshot=data.get("title_snapshot", ""),
            content_snapshot=data.get("content_snapshot", ""),
            change_comment=data.get("change_comment"),
            is_current=data.get("is_current", False),
            is_archived=data.get("is_archived", False),
            section_id=data["section_id"],
            author_id=data["author_id"],
            created_at=created_at,
            change_type=data.get("change_type", ""),
        )