from core.schema import CategoryResult

class RagPrivacyAudit:
    name = "RAG Privacy"

    @staticmethod
    def evaluate(answers):
        findings, recommendations, score = [], [], 10

        if answers.get("rag_sources_private") == "No":
            findings.append("RAG model pulls from non-private or public sources.")
            recommendations.append("Restrict RAG data stores to approved private indexes only.")
            score -= 4

        if answers.get("pii_redaction") == "No":
            findings.append("No PII redaction before RAG ingestion.")
            recommendations.append("Enable automated PII scrubbing or filtering in pipeline.")
            score -= 3

        if answers.get("rag_cache_purge") == "No":
            findings.append("RAG retrieval cache not periodically cleared.")
            recommendations.append("Schedule automatic cache purges to limit data retention.")
            score -= 2

        return CategoryResult("RAG Privacy", max(score, 0), findings, recommendations)
