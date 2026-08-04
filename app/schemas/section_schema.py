"""
Section Pydantic schemas.

This module defines the request and response schemas
used by the Section Management API.
"""

from pydantic import BaseModel, ConfigDict

from app.enums.section_status import SectionStatus


class SectionCreate(BaseModel):
    """
    Schema used to create a new section.

    A section belongs to a document and a project.
    The assigned user is optional because the project manager
    can assign a collaborator later.
    """

    # Section title extracted from the Word document
    title: str

    # Editable content of the section
    # This field will later be modified by the collaborative editor
    content: str

    # Heading level in the document structure
    # Example:
    # 1 -> Heading 1
    # 2 -> Heading 2
    level: int

    # Position of the section inside the document
    # Used to keep the original Word document order
    order: int

    # Functional module of the section
    # Example:
    # "Backend", "Frontend", "Database"
    module: str


    # Document containing this section
    document_id: int

    # Project owning this section
    project_id: int


    # User responsible for editing this section
    # Optional because assignment can happen later
    assigned_user_id: int | None = None



class SectionUpdate(BaseModel):
    """
    Schema used to update an existing section.

    Only provided fields will be modified.
    """

    # Update section title if needed
    title: str | None = None

    # Update section content
    # This will be the main field modified by the editor
    content: str | None = None


    # Change workflow status
    # Example:
    # IN_PROGRESS
    # COMPLETED
    status: SectionStatus | None = None


    # Assign or change the responsible collaborator
    assigned_user_id: int | None = None



class SectionResponse(BaseModel):
    """
    Schema returned by the API.

    This schema represents a section sent back
    to the frontend application.
    """


    # Unique identifier
    id: int


    # Section information
    title: str
    content: str


    # Word document structure information
    level: int
    order: int
    module: str


    # Current workflow status
    status: SectionStatus


    # Indicates if another user is currently editing
    # Used later for collaborative locking
    is_locked: bool


    # Relations
    document_id: int
    project_id: int


    # Current collaborator responsible for this section
    # None means that the section is not assigned yet
    assigned_user_id: int | None



    # Allows Pydantic to read SQLAlchemy objects directly
    # Example:
    # section.id -> id
    # section.title -> title
    model_config = ConfigDict(
        from_attributes=True
    )