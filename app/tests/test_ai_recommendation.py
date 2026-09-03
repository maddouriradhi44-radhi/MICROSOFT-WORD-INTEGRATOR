from app.services.ai.ai_recommendation_service import (
    AIRecommendationService,
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


confidence_result = {
    "score": 0.85,
    "level": "high",
}


service = AIRecommendationService()

result = service.recommend(
    comparison=comparison,
    risk_result=risk_result,
    confidence_result=confidence_result,
)


print()
print("===== AI RECOMMENDATION =====")
print()

print("Recommendation:", result["recommendation"])
print("Reason:", result["reason"])