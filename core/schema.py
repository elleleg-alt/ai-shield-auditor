
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Finding(BaseModel):
    text: str
    severity: str = Field(default="Medium")  # Low, Medium, High
    evidence: Optional[str] = None

class Recommendation(BaseModel):
    text: str
    effort: str = Field(default="Medium")  # Low, Medium, High

class CategoryResult(BaseModel):
    category: str
    score: float  # 0..10
    risk_level: str  # Low/Medium/High
    questions: List[str]
    answers: Dict[str, str]
    findings: List[Finding]
    recommendations: List[Recommendation]

class UserEnvironment(BaseModel):
    platform: str
    agent_mode: bool
    connectors: List[str]
    vector_store: Optional[str] = None
    sensitive_data_types: List[str] = []

class AuditReport(BaseModel):
    user_environment: UserEnvironment
    audit_categories: List[CategoryResult]
    summary: Dict[str, str]

    def overall_score(self) -> float:
        if not self.audit_categories:
            return 0.0
        return round(sum(c.score for c in self.audit_categories) / len(self.audit_categories), 2)

    def overall_risk(self) -> str:
        # Map overall score to risk
        s = self.overall_score()
        if s >= 8.5:
            return "Low"
        if s >= 6.5:
            return "Moderate"
        return "High"

    def meta(self) -> Dict[str, str]:
        return {
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "overall_score": str(self.overall_score()),
            "overall_risk": self.overall_risk(),
        }
