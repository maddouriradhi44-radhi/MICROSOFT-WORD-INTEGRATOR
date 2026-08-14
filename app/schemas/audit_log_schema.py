"""
Audit log schemas.

This module defines schemas used by the Audit API.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    """
    Response schema for an audit log entry.
    """

    id: int
    action: str
    target: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)