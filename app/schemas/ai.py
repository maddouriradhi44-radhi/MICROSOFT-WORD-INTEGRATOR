from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator




class AISubsectionProposal(BaseModel):
    """
    AI-generated proposal for a logical subsection.
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

    category: str | None = None

    suggested_role: str | None = None

    keywords: list[str] = Field(
        default_factory=list,
    )

    complexity: str = "medium"


class AISectionProposal(BaseModel):
    """
    AI-generated logical section proposal.
    """

    title: str

    level: int = Field(
        ge=1,
    )

    content: str

    order: int = Field(
        ge=1,
    )

    reason: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    category: str | None = None

    suggested_role: str | None = None

    keywords: list[str] = Field(
        default_factory=list,
    )

    complexity: str = "medium"

    subsections: list[AISubsectionProposal] = Field(
        default_factory=list,
    )


class AIDocumentProposal(BaseModel):
    """
    AI-generated logical decomposition proposal
    for a complete DOCX document.

    This is only a proposal.
    It does not create database sections automatically.
    """

    document_title: str

    sections: list[AISectionProposal] = Field(
        default_factory=list,
    )

    reason: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


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


class AISectionProposalResponse(BaseModel):
    """
    Schema returned by the API for an AI section proposal.
    """

    id: int

    document_id: int

    section_id: int | None = None

    title: str

    content: str | None = None

    level: int | None = None

    order: int | None = None

    reason: str

    confidence: float

    category: str | None = None

    suggested_role: str | None = None

    keywords: list[str] = Field(
        default_factory=list,
    )

    complexity: str

    status: str

    reviewed_by: int | None = None

    reviewed_at: datetime | None = None

    review_comment: str | None = None

    @field_validator("keywords", mode="before")
    @classmethod
    def parse_keywords(cls, value):
        if value is None:
            return []

        if isinstance(value, str):
            return [
                keyword.strip()
                for keyword in value.split(",")
                if keyword.strip()
            ]

        return value

    model_config = ConfigDict(
        from_attributes=True,
    )

class AISectionProposalUpdate(BaseModel):
    """
    Fields that can be modified by the Project Manager
    before accepting or rejecting an AI proposal.
    """

    title: str | None = None

    content: str | None = None

    level: int | None = Field(
        default=None,
        ge=1,
    )

    order: int | None = Field(
        default=None,
        ge=1,
    )

    category: str | None = None

    suggested_role: str | None = None

    keywords: list[str] | None = None

    complexity: str | None = None

    review_comment: str | None = None


class AISectionProposalReject(BaseModel):
    """
    Data used when rejecting an AI proposal.
    """

    review_comment: str | None = None


class AIValidationReportResponse(BaseModel):
    """
    Schema returned by the API for an AI validation report.
    """

    id: int

    validation_id: int

    analysis_status: str

    summary: str | None = None

    addition_count: int

    deletion_count: int

    modification_count: int

    important_changes: list = Field(
        default_factory=list,
    )

    risks: list = Field(
        default_factory=list,
    )

    confidence_score: float

    confidence_level: str

    coherence_score: float

    coherence_level: str

    coherence_issues: list = Field(
        default_factory=list,
    )

    coherence_summary: str | None = None

    recommendation: str

    recommendation_reason: str | None = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
