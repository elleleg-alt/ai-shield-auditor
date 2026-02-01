
from core.schema import CategoryResult

class IdentityAccessAudit:
    name = "Identity & Access"

    @staticmethod
    def evaluate(answers):
        findings = []
        recommendations = []
        score = 10

        if answers.get("mfa_enabled") == "No":
            findings.append("Multi-factor authentication is disabled.")
            recommendations.append("Enable MFA for all administrative and developer accounts.")
            score -= 4

        if answers.get("key_rotation") == "No":
            findings.append("No key rotation policy detected.")
            recommendations.append("Implement automatic key rotation every 90 days.")
            score -= 3

        if answers.get("privileged_access_review") == "No":
            findings.append("Privileged access reviews not in place.")
            recommendations.append("Establish periodic access reviews for privileged users.")
            score -= 2

        return CategoryResult(
            category="Identity & Access",
            score=max(score, 0),
            findings=findings,
            recommendations=recommendations,
        )
