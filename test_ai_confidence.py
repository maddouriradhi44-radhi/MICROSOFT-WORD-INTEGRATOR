from app.services.ai.ai_confidence_service import (
    AIConfidenceService,
)


comparison = {
    "additions": [
        "MODIFICATION TEST REJET",
        "Cette modification doit être rejetée par le Project Manager.",
    ],
    "deletions": [],
    "modifications": [],
}


risk_result = {
    "has_risk": True,
    "risks": [
        {
            "type": "suspicious_content",
            "severity": "medium",
            "message": (
                "Potentially suspicious content "
                "was detected."
            ),
            "content": "MODIFICATION TEST REJET",
        }
    ],
}


service = AIConfidenceService()

result = service.calculate_confidence(
    comparison=comparison,
    risk_result=risk_result,
)


print()
print("===== AI CONFIDENCE =====")
print()

print("Score:", result["score"])
print("Level:", result["level"])