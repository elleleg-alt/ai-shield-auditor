
from typing import Dict, Any, List
from pydantic import BaseModel
from core.schema import CategoryResult, Finding, Recommendation
from core.scoring import score_yes_no_answers, risk_from_score

class ComplianceAudit:
    NAME = "Compliance"

    def questions(self) -> List[str]:
        return template_questions

    def evaluate(self, answers: Dict[str, str]) -> CategoryResult:
        score = score_yes_no_answers(answers)
        risk = risk_from_score(score)
        findings = []
        recs = []

        # Simple heuristics for examples
        for q, a in answers.items():
            a_norm = (a or "").strip().lower()
            if "mfa" in q.lower() and a_norm in ("no", "unknown"):
                findings.append(Finding(text="MFA not enforced for admins/users.", severity="High"))
                recs.append(Recommendation(text="Enforce MFA via IdP or conditional access.", effort="Low"))
            if "public" in q.lower() and a_norm in ("yes",):
                findings.append(Finding(text="Public storage detected for logs/embeddings.", severity="High"))
                recs.append(Recommendation(text="Make buckets private and add KMS encryption.", effort="Low"))

        return CategoryResult(
            category=self.NAME,
            score=score,
            risk_level=risk,
            questions=list(answers.keys()),
            answers=answers,
            findings=findings,
            recommendations=recs,
        )

# Placeholder; template_questions will be injected by app.py from YAML at runtime.
template_questions: List[str] = []
