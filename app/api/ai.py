"""
AI API.

This module exposes endpoints
for AI-generated section proposals.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.dependencies.auth_dependency import (
    get_current_user,
)

from app.models.user import User

from app.schemas.ai import (
    AISectionProposal,
    AISectionProposalResponse,
    AISectionProposalUpdate,
    AISectionProposalReject,
    AIValidationReportResponse,
)

from app.services.ai.ai_section_analysis_service import (
    AISectionAnalysisService,
)

from app.services.ai.ai_section_proposal_service import (
    AISectionProposalService,
)

from app.services.section_service import (
    SectionService,
)

from app.models.ai_validation_report import (
    AIValidationReport,
)

from app.models.validation import Validation
from app.models.version import Version


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


ai_analysis_service = AISectionAnalysisService()
ai_proposal_service = AISectionProposalService()
section_service = SectionService()


# ==========================================================
# ANALYZE SECTION
# ==========================================================

@router.post(
    "/sections/{section_id}/analyze",
    response_model=AISectionProposalResponse,
)
def analyze_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze a section with the AI
    and save the generated proposal.
    """

    # ------------------------------------------------------
    # Get section
    # ------------------------------------------------------

    section = section_service.get_section_by_id(
        db,
        section_id,
    )

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )

    # ------------------------------------------------------
    # Prepare section data for AI
    # ------------------------------------------------------

    section_data = {
        "title": section.title,
        "content": section.content,
        "level": section.level,
    }

    # ------------------------------------------------------
    # AI analysis
    # ------------------------------------------------------

    proposal = ai_analysis_service.analyze_section(
        section_data,
    )

    # ------------------------------------------------------
    # Save proposal
    # ------------------------------------------------------

    ai_proposal = ai_proposal_service.create_proposal(
        db=db,
        document_id=section.document_id,
        proposal=proposal,
    )

    # ------------------------------------------------------
    # Return AI proposal
    # ------------------------------------------------------

    return ai_proposal


# ==========================================================
# GET DOCUMENT PROPOSALS
# ==========================================================

@router.get(
    "/documents/{document_id}/proposals",
    response_model=list[AISectionProposalResponse],
)
def get_document_proposals(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all AI section proposals for a document.
    """

    proposals = ai_proposal_service.get_document_proposals(
        db=db,
        document_id=document_id,
    )

    return proposals


# ==========================================================
# UPDATE PROPOSAL
# ==========================================================

@router.patch(
    "/proposals/{proposal_id}",
    response_model=AISectionProposalResponse,
)
def update_proposal(
    proposal_id: int,
    data: AISectionProposalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Modify an AI proposal before acceptance or rejection.

    Only the Project Manager can modify a proposal.
    """

    try:
        proposal = ai_proposal_service.update_proposal(
            db=db,
            proposal_id=proposal_id,
            user_id=current_user.id,
            title=data.title,
            content=data.content,
            level=data.level,
            order=data.order,
            category=data.category,
            suggested_role=data.suggested_role,
            keywords=data.keywords,
            complexity=data.complexity,
            review_comment=data.review_comment,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "AI proposal not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return proposal


# ==========================================================
# ACCEPT PROPOSAL
# ==========================================================

@router.post(
    "/proposals/{proposal_id}/accept",
)
def accept_proposal(
    proposal_id: int,
    assigned_user_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Accept an AI proposal and create the corresponding Section.

    The AI does NOT assign collaborators automatically.
    """

    try:
        section = ai_proposal_service.accept_proposal(
            db=db,
            proposal_id=proposal_id,
            user_id=current_user.id,
            assigned_user_id=assigned_user_id,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "AI proposal not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return {
        "message": "AI proposal accepted",
        "proposal_id": proposal_id,
        "section_id": section.id,
    }


# ==========================================================
# REJECT PROPOSAL
# ==========================================================

@router.post(
    "/proposals/{proposal_id}/reject",
    response_model=AISectionProposalResponse,
)
def reject_proposal(
    proposal_id: int,
    data: AISectionProposalReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Reject an AI proposal.

    Rejection does not create a real Section.
    """

    try:
        proposal = ai_proposal_service.reject_proposal(
            db=db,
            proposal_id=proposal_id,
            user_id=current_user.id,
            review_comment=data.review_comment,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "AI proposal not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return proposal


# ==========================================================
# GET VALIDATION AI REPORT
# ==========================================================

@router.get(
    "/validations/{validation_id}/report",
    response_model=AIValidationReportResponse,
)
def get_validation_ai_report(
    validation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the AI validation report associated
    with a validation.
    """

    report = (
        db.query(AIValidationReport)
        .filter(
            AIValidationReport.validation_id
            == validation_id
        )
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="AI validation report not found",
        )

    return report


# ==========================================================
# GET SECTION AI VALIDATION REPORT
# ==========================================================

@router.get(
    "/sections/{section_id}/validation-report",
    response_model=AIValidationReportResponse,
)
def get_section_ai_validation_report(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the latest AI validation report
    associated with a section.
    """

    report = (
        db.query(AIValidationReport)
        .join(
            AIValidationReport.validation
        )
        .join(
            Validation.version
        )
        .filter(
            Version.section_id == section_id
        )
        .order_by(
            AIValidationReport.created_at.desc()
        )
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="AI validation report not found",
        )

    return report