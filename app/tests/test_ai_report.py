from app.database.session import SessionLocal

from app.repositories.version_repository import (
    VersionRepository,
)

from app.services.ai.ai_report_service import (
    AIReportService,
)


db = SessionLocal()

try:

    repository = VersionRepository()

    old_version = repository.get_version_by_id(
        db,
        13,
    )

    new_version = repository.get_version_by_id(
        db,
        14,
    )

    if old_version is None:
        print("Old version not found")
        raise SystemExit

    if new_version is None:
        print("New version not found")
        raise SystemExit

    service = AIReportService()

    report = service.generate_report(
        old_version=old_version,
        new_version=new_version,
    )

    print()
    print("===== AI COMPLETE REPORT =====")
    print()

    print(
        f"Section: {report['section_id']}"
    )

    print(
        f"Old version: "
        f"v{report['old_version']['version_number']}"
    )

    print(
        f"New version: "
        f"v{report['new_version']['version_number']}"
    )

    print()
    print("--- SUMMARY ---")
    print(
        report["summary"]["summary"]
    )

    print()
    print("--- CHANGES ---")
    print(
        f"Additions: "
        f"{report['summary']['addition_count']}"
    )

    print(
        f"Deletions: "
        f"{report['summary']['deletion_count']}"
    )

    print(
        f"Modifications: "
        f"{report['summary']['modification_count']}"
    )

    print()
    print("--- RISKS ---")

    print(
        f"Has risk: "
        f"{report['risks']['has_risk']}"
    )

    for risk in report["risks"]["risks"]:

        print(
            f"Type: {risk['type']}"
        )

        print(
            f"Severity: {risk['severity']}"
        )

        print(
            f"Message: {risk['message']}"
        )

        print()

    print("--- CONFIDENCE ---")

    print(
        f"Score: "
        f"{report['confidence']['score']}"
    )

    print(
        f"Level: "
        f"{report['confidence']['level']}"
    )

    print()
    print("--- RECOMMENDATION ---")

    print(
        f"Recommendation: "
        f"{report['recommendation']['recommendation']}"
    )

    print(
        f"Reason: "
        f"{report['recommendation']['reason']}"
    )

finally:
    db.close()