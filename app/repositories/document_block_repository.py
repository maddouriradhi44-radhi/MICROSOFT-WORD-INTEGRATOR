"""
Document block repository.

This module handles database operations
related to document blocks.
"""


from sqlalchemy.orm import Session

from app.models.document_block import DocumentBlock



class DocumentBlockRepository:
    """
    Database operations related to document blocks.
    """



    def create_block(
        self,
        db: Session,
        block: DocumentBlock,
    ) -> DocumentBlock:
        """
       Save a new document block into the database.
        """

        db.add(block)
        db.commit()
        db.refresh(block)

        return block



    def get_block_by_id(
        self,
        db: Session,
        block_id: int,
    ) -> DocumentBlock | None:
        """
        Retrieve a block by its identifier.
        """

        return (
            db.query(DocumentBlock)
            .filter(
                DocumentBlock.id == block_id
            )
            .first()
        )



    def get_section_blocks(
        self,
        db: Session,
        section_id: int,
    ) -> list[DocumentBlock]:
        """
        Retrieve all blocks belonging to a section
        ordered by their position.
        """

        return (
            db.query(DocumentBlock)
            .filter(
                DocumentBlock.section_id == section_id
            )
            .order_by(
                DocumentBlock.order_index
            )
            .all()
        )



    def update_block(
        self,
        db: Session,
        block: DocumentBlock,
        updates: dict,
    ) -> DocumentBlock:
        """
        Update an existing document block.
        """

        for field, value in updates.items():
            setattr(
                block,
                field,
                value,
            )

        db.commit()
        db.refresh(block)

        return block



    def delete_block(
        self,
        db: Session,
        block: DocumentBlock,
    ) -> bool:
        """
        Delete a document block.
        """

        db.delete(block)
        db.commit()

        return True