"""
AI collaborator profile service.

Builds an AI-oriented profile for project collaborators.
"""

from __future__ import annotations

from app.schemas.ai import AICollaboratorProfile


class AICollaboratorProfileService:
    """
    Service responsible for building AI collaborator profiles.
    """

    def build_profile(
        self,
        user_id: int,
        skills: list[str] | None = None,
        experience_level: str = "medium",
        languages: list[str] | None = None,
        preferred_roles: list[str] | None = None,
        availability: str = "available",
    ) -> AICollaboratorProfile:
        """
        Build an AI profile for a collaborator.
        """

        return AICollaboratorProfile(
            user_id=user_id,
            skills=skills or [],
            experience_level=experience_level,
            languages=languages or [],
            preferred_roles=preferred_roles or [],
            availability=availability,
        )