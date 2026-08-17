from pydantic import BaseModel, Field


class AISectionProposal(BaseModel):
    """
    AI-generated proposal for a document section.
    """

    title: str

    level: int = Field(
        ge=1,
    )

    content: str

    reason: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    suggested_role: str | None = None

    keywords: list[str] = []

    complexity: str = "medium"


class AIDocumentClassification(BaseModel):
    """
    AI-generated classification of a DOCX document.
    """

    document_type: str

    language: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

class AICollaboratorProfile(BaseModel):
    """
    AI profile used to evaluate a collaborator
    for a section assignment recommendation.
    """

    user_id: int

    skills: list[str] = Field(
        default_factory=list,
    )

    experience_level: str = "medium"

    languages: list[str] = Field(
        default_factory=list,
    )

    preferred_roles: list[str] = Field(
        default_factory=list,
    )

    availability: str = "available"

