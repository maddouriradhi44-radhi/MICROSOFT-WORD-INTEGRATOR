"""
Document block schemas.

This module defines request and response schemas
used by the Document Block API.
"""


from pydantic import BaseModel, ConfigDict



class DocumentBlockCreate(BaseModel):
    """
    Schema used to create a new document block.
    """


    # Section containing this block
    section_id: int


    # Type of Word element
    # Examples: paragraph, heading, table, image, list
    type: str


    # Original OOXML fragment from Word
    # Used to preserve formatting
    content_xml: str


    # Position inside the section
    # Examples: 1.0, 2.0, 2.5
    order_index: float




class DocumentBlockUpdate(BaseModel):
    """
    Schema used to update an existing document block.
    """


    # Update block type if needed
    type: str | None = None


    # Update OOXML content
    content_xml: str | None = None


    # Update block position
    order_index: float | None = None




class DocumentBlockResponse(BaseModel):
    """
    Schema returned by the API.
    """

    # Unique identifier
    id: int
    # Parent section
    section_id: int
    # Word block type
    type: str
    # Original Word OOXML
    content_xml: str
    # Block position
    order_index: float
    # Allow Pydantic to read SQLAlchemy objects
    model_config = ConfigDict(
        from_attributes=True
    )

    