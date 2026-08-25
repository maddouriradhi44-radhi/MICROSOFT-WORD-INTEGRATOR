from app.ui.models.ai_section_proposal import (
    AISectionProposal,
)


class AISectionProposalService:
    """
    Temporary frontend service for AI section proposals.

    The current implementation uses local mock data.

    Later, this service can be replaced by an API call
    without changing the proposal screen.
    """

    def get_proposals(
        self,
        document_id=None,
    ) -> list[AISectionProposal]:

        mock_data = [
            {
                "title": "Introduction",
                "level": 1,
                "content": (
                    "Présentation générale du projet, "
                    "de son contexte et de ses objectifs."
                ),
                "reason": (
                    "Cette partie présente le contexte général "
                    "et les objectifs du document."
                ),
                "confidence": 0.92,
                "suggested_role": "functional",
                "keywords": [
                    "project",
                    "objectives",
                    "introduction",
                ],
                "complexity": "low",
            },
            {
                "title": "Functional Requirements",
                "level": 1,
                "content": (
                    "Description des fonctionnalités attendues "
                    "et des besoins fonctionnels du système."
                ),
                "reason": (
                    "Les exigences fonctionnelles sont regroupées "
                    "dans une section cohérente."
                ),
                "confidence": 0.95,
                "suggested_role": "functional",
                "keywords": [
                    "requirements",
                    "features",
                    "functional",
                ],
                "complexity": "medium",
            },
            {
                "title": "Technical Architecture",
                "level": 1,
                "content": (
                    "Architecture backend, API, base de données "
                    "et organisation technique du système."
                ),
                "reason": (
                    "Cette partie regroupe les informations "
                    "relatives à l'architecture technique."
                ),
                "confidence": 0.89,
                "suggested_role": "technical",
                "keywords": [
                    "architecture",
                    "api",
                    "backend",
                    "database",
                ],
                "complexity": "medium",
            },
            {
                "title": "Authentication and Authorization",
                "level": 2,
                "content": (
                    "Gestion de l'authentification, des rôles "
                    "et des permissions utilisateurs."
                ),
                "reason": (
                    "Cette partie décrit les mécanismes "
                    "de sécurité et de contrôle d'accès."
                ),
                "confidence": 0.87,
                "suggested_role": "technical",
                "keywords": [
                    "authentication",
                    "authorization",
                    "security",
                ],
                "complexity": "medium",
            },
            {
                "title": "Database Design",
                "level": 2,
                "content": (
                    "Structure de la base de données, tables, "
                    "relations et contraintes."
                ),
                "reason": (
                    "Les éléments concernant la persistance "
                    "des données sont regroupés ici."
                ),
                "confidence": 0.84,
                "suggested_role": "technical",
                "keywords": [
                    "database",
                    "schema",
                    "tables",
                    "relations",
                ],
                "complexity": "high",
            },
            {
                "title": "Testing and Quality Assurance",
                "level": 1,
                "content": (
                    "Stratégie de tests, validation fonctionnelle "
                    "et contrôle de la qualité du système."
                ),
                "reason": (
                    "Cette partie regroupe les activités liées "
                    "aux tests et à la qualité."
                ),
                "confidence": 0.91,
                "suggested_role": "qa",
                "keywords": [
                    "testing",
                    "quality",
                    "validation",
                ],
                "complexity": "medium",
            },
            {
                "title": "Project Management",
                "level": 1,
                "content": (
                    "Organisation du projet, suivi des tâches, "
                    "planning et gestion des livrables."
                ),
                "reason": (
                    "Cette partie décrit les aspects "
                    "organisationnels du projet."
                ),
                "confidence": 0.78,
                "suggested_role": "management",
                "keywords": [
                    "planning",
                    "tasks",
                    "management",
                ],
                "complexity": "low",
            },
        ]

        return [
            AISectionProposal.from_dict(
                data,
                order=index + 1,
            )
            for index, data in enumerate(
                mock_data
            )
        ]


ai_section_proposal_service = (
    AISectionProposalService()
)