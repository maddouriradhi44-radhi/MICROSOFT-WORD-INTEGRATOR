from types import SimpleNamespace

from app.enums.ai_analysis_status import AIAnalysisStatus
from app.services.ai.ai_analysis_status_service import (
    AIAnalysisStatusService,
)


class FakeDB:
    def add(self, obj):
        pass

    def commit(self):
        pass

    def refresh(self, obj):
        pass


db = FakeDB()


# ==========================================================
# PENDING -> IN_PROGRESS
# ==========================================================

report = SimpleNamespace(
    analysis_status=AIAnalysisStatus.PENDING,
)

AIAnalysisStatusService.set_status(
    db,
    report,
    AIAnalysisStatus.IN_PROGRESS,
)

print(
    "PENDING -> IN_PROGRESS:",
    report.analysis_status,
)


# ==========================================================
# IN_PROGRESS -> COMPLETED
# ==========================================================

AIAnalysisStatusService.set_status(
    db,
    report,
    AIAnalysisStatus.COMPLETED,
)

print(
    "IN_PROGRESS -> COMPLETED:",
    report.analysis_status,
)


# ==========================================================
# IN_PROGRESS -> FAILED
# ==========================================================

report = SimpleNamespace(
    analysis_status=AIAnalysisStatus.IN_PROGRESS,
)

AIAnalysisStatusService.set_status(
    db,
    report,
    AIAnalysisStatus.FAILED,
)

print(
    "IN_PROGRESS -> FAILED:",
    report.analysis_status,
)


# ==========================================================
# INVALID TRANSITION
# ==========================================================

report = SimpleNamespace(
    analysis_status=AIAnalysisStatus.PENDING,
)

try:
    AIAnalysisStatusService.set_status(
        db,
        report,
        AIAnalysisStatus.COMPLETED,
    )

    print(
        "ERROR: invalid transition was accepted!"
    )

except ValueError as exc:
    print(
        "PENDING -> COMPLETED: BLOCKED",
        exc,
    )