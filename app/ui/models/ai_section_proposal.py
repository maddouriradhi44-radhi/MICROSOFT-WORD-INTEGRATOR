from dataclasses import dataclass, field
from typing import Any


@dataclass
class AISectionProposal:
    """
    Frontend model representing an AI-generated section proposal.

    This is NOT an official Section.

    The AI only proposes a logical document decomposition.
    The Project Manager remains responsible for modifying,
    reorganizing and validating the proposal.
    """

    title: str
    level: int
    content: str
    reason: str
    confidence: float
    suggested_role: str
    keywords: list[str] = field(default_factory=list)
    complexity: str = "medium"

    # Frontend-only state
    order: int = 0
    selected: bool = False
    is_modified: bool = False
    is_ai_generated: bool = True

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        order: int = 0,
    ) -> "AISectionProposal":

        return cls(
            title=data.get("title", ""),
            level=data.get("level", 0),
            content=data.get("content", ""),
            reason=data.get("reason", ""),
            confidence=float(
                data.get("confidence", 0.0)
            ),
            suggested_role=data.get(
                "suggested_role",
                "",
            ),
            keywords=data.get(
                "keywords",
                [],
            ),
            complexity=data.get(
                "complexity",
                "medium",
            ),
            order=order,
            selected=False,
            is_modified=False,
            is_ai_generated=True,
        )

    @property
    def confidence_percentage(self) -> int:
        """
        Convert AI confidence from 0.0-1.0
        to a percentage for display.
        """
        return round(
            self.confidence * 100
        )
    