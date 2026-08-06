"""
Version schemas.

This module defines Pydantic schemas
used for version management.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict
from app.enums.version_change import VersionChangeType


class VersionCreate(BaseModel):
    """
    Schema used to create a new version.
    """

    section_id: int

    title_snapshot: str

    content_snapshot: str

    change_comment: str | None = None



class VersionResponse(BaseModel):
    """
    Schema used to return version information.
    """

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

    change_type: VersionChangeType


    model_config = ConfigDict(
        from_attributes=True
    )



class VersionHistoryResponse(BaseModel):
    """
    Schema used to return version history.
    """

    versions: list[VersionResponse]



class VersionRestore(BaseModel):
    """
    Schema used to restore a version.
    """

    version_id: int