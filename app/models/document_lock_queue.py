"""
Document Lock Queue model.

Handles users waiting to edit a locked document.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.lock_request_status import LockRequestStatus


if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.user import User


class DocumentLockQueue(Base):

    __tablename__ = "document_lock_queue"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


    requested_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


    status: Mapped[LockRequestStatus] = mapped_column(
        Enum(LockRequestStatus),
        default=LockRequestStatus.WAITING,
        nullable=False,
    )


    document: Mapped["Document"] = relationship(
        back_populates="lock_queue"
    )


    user: Mapped["User"] = relationship(
        back_populates="document_lock_queue"
    )

    notified_at: Mapped[datetime | None] = mapped_column(
    DateTime,
    nullable=True,
)