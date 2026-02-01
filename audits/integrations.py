
from core.schema import CategoryResult

class IntegrationsAudit:
    name = "Integrations"

    @staticmethod
    def evaluate(answers):
        findings, recommendations, score = [], [], 10

        if answers.get("third_party_integrations") == "Yes":
            if answers.get("integration_reviewed") == "No":
                findings.append("Third-party integrations not security reviewed.")
                recommendations.append("Perform security review for all connected integrations.")
                score -= 3

            if answers.get("scopes_limited") == "No":
                findings.append("Integrations have excessive permission scopes.")
                recommendations.append("Restrict API scopes to minimum required privileges.")
                score -= 2

        if answers.get("integration_logging") == "No":
            findings.append("No activity logging for integrated apps.")
            recommendations.append("Enable audit logging for all third-party integrations.")
            score -= 3

        return CategoryResult("Integrations", max(score, 0), findings, recommendations)
