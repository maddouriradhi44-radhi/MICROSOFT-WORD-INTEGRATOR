from app.database.session import SessionLocal

from app.repositories.version_repository import VersionRepository
from app.services.ai.ai_version_comparison_service import (
    AIVersionComparisonService,
)


db = SessionLocal()

try:
    repository = VersionRepository()
    service = AIVersionComparisonService()

    old_version = repository.get_version_by_id(
        db,
        13,
    )

    new_version = repository.get_version_by_id(
        db,
        14,
    )

    if old_version is None:
        print("ERROR: Version 13 not found")
    elif new_version is None:
        print("ERROR: Version 14 not found")
    else:
        result = service.compare_versions(
            old_version,
            new_version,
        )

        print("\n===== AI VERSION COMPARISON =====")

        print(
            f"Old version: "
            f"v{result['old_version_number']}"
        )

        print(
            f"New version: "
            f"v{result['new_version_number']}"
        )

        print(
            f"Has changes: "
            f"{result['has_changes']}"
        )

        print("\n--- ADDITIONS ---")

        for item in result["additions"]:
            print(f"+ {item}")

        print("\n--- DELETIONS ---")

        for item in result["deletions"]:
            print(f"- {item}")

        print("\n--- MODIFICATIONS ---")

        for modification in result["modifications"]:
            print("OLD:")
            for line in modification["old"]:
                print(f"  - {line}")

            print("NEW:")
            for line in modification["new"]:
                print(f"  + {line}")

finally:
    db.close()