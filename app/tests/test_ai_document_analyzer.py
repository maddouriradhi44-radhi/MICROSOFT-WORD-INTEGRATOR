from app.services.ai.ai_document_analyzer_service import (
    AIDocumentAnalyzerService,
)


def main():

    sections = [
        {
            "title": "Introduction",
            "content": (
                "This document presents the collaborative "
                "software project and its objectives."
            ),
            "level": 1,
        },
        {
            "title": "Technical Architecture",
            "content": (
                "The backend uses Python and FastAPI. "
                "The application exposes a REST API and "
                "uses PostgreSQL as the database."
            ),
            "level": 1,
        },
        {
            "title": "Testing and Validation",
            "content": (
                "The application must be tested and validated "
                "to guarantee software quality."
            ),
            "level": 1,
        },
    ]

    analyzer = AIDocumentAnalyzerService()

    proposals = analyzer.analyze_document(
        sections
    )

    print()
    print("=" * 60)
    print("AI DOCUMENT ANALYSIS")
    print("=" * 60)

    for index, proposal in enumerate(
        proposals,
        start=1,
    ):

        print()
        print(f"SECTION {index}")
        print("-" * 40)

        print("Title:", proposal.title)
        print("Level:", proposal.level)
        print("Role:", proposal.suggested_role)
        print("Keywords:", proposal.keywords)
        print("Complexity:", proposal.complexity)
        print("Confidence:", proposal.confidence)
        print("Reason:", proposal.reason)


if __name__ == "__main__":
    main()