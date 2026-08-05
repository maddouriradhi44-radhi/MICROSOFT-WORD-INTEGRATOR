"""
Document block service.

This module contains business logic
related to document blocks.
"""


from sqlalchemy.orm import Session


from app.models.document_block import DocumentBlock

from app.repositories.document_block_repository import (
    DocumentBlockRepository,
)

from app.schemas.document_block_schema import (
    DocumentBlockCreate,
    DocumentBlockUpdate,
)


class DocumentBlockService:
    """
    Business logic related to document blocks.
    """


    def __init__(self):
        self.repository = DocumentBlockRepository()

     
    # CREATE BLOCK
    def create_block(
        self,
        db: Session,
        block_data: DocumentBlockCreate,
    ) -> DocumentBlock:
        """
        Create a new document block.
        """


        block = DocumentBlock(
            section_id=block_data.section_id,
            type=block_data.type,
            content_xml=block_data.content_xml,
            order_index=block_data.order_index,
        )


        return self.repository.create_block(
            db,
            block,
        )

    # GET BLOCK BY ID
    def get_block_by_id(
        self,
        db: Session,
        block_id: int,
    ) -> DocumentBlock | None:
        """
        Retrieve a block by id.
        """


        return self.repository.get_block_by_id(
            db,
            block_id,
        )

 
    # GET SECTION BLOCKS
    def get_section_blocks(
        self,
        db: Session,
        section_id: int,
    ) -> list[DocumentBlock]:
        """
        Retrieve all blocks of a section.
        """


        return self.repository.get_section_blocks(
            db,
            section_id,
        )


    # UPDATE BLOCK
    def update_block(
        self,
        db: Session,
        block_id: int,
        block_data: DocumentBlockUpdate,
    ) -> DocumentBlock | None:
        """
        Update an existing document block.
        """


        block = self.repository.get_block_by_id(
            db,
            block_id,
        )


        if block is None:
            return None



        updates = block_data.model_dump(
            exclude_unset=True
        )


        return self.repository.update_block(
            db,
            block,
            updates,
        )


    # DELETE BLOCK

    def delete_block(
        self,
        db: Session,
        block_id: int,
    ) -> bool:
        """
        Delete a document block.
        """


        block = self.repository.get_block_by_id(
            db,
            block_id,
        )


        if block is None:
            return False

        self.repository.delete_block(
            db,
            block,
        )
        return True