from dataclasses import dataclass


@dataclass
class Project:
    id: int
    name: str
    description: str | None
    status: str
    owner_id: int
    created_at: str | None
    role: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            status=data["status"],
            owner_id=data["owner_id"],
            created_at=data.get("created_at"),
            role=data["role"],
        )