"""
Document Lock model.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.user import User


class DocumentLock(Base):

    __tablename__ = "document_locks"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        unique=True
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )


    locked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )


    document: Mapped["Document"] = relationship(
        back_populates="lock"
    )


    user: Mapped["User"] = relationship(
        back_populates="document_locks"
    )