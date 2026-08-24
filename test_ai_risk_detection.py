from app.services.ai.ai_risk_detection_service import (
    AIRiskDetectionService,
)


comparison = {
    "additions": [
        "MODIFICATION TEST REJET",
        "Cette modification doit être rejetée par le Project Manager.",
    ],
    "deletions": [],
    "modifications": [],
}


service = AIRiskDetectionService()

result = service.detect_risks(
    comparison
)


print()
print("===== AI RISK DETECTION =====")
print()

print("Has risk:", result["has_risk"])

print()
print("Risks:")

for risk in result["risks"]:
    print()
    print("Type:", risk["type"])
    print("Severity:", risk["severity"])
    print("Message:", risk["message"])
    print("Content:", risk.get("content"))