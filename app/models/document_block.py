from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
    Text,
    Float,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.section import Section



class DocumentBlock(Base):
    """
    Represents a technical block extracted from a Word document section.

    A block keeps the original OOXML content to preserve
    Word formatting during document reconstruction.
    """

    __tablename__ = "document_blocks"


    # Unique identifier of the document block
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    # Section containing this block
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.id"),
        nullable=False
    )


    # Type of block extracted from Word
    # Examples: paragraph, heading, table, image, list
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    # Original Word OOXML fragment
    # Used to preserve formatting during export
    content_xml: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    # Position of the block inside the section
    # Uses fractional indexing to avoid massive reordering
    # Examples: 1.0, 2.0, 2.5
    order_index: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    # Parent section relationship
    section: Mapped["Section"] = relationship(
        back_populates="blocks"
    )