
from typing import Dict, Tuple

def risk_from_score(score: float) -> str:
    if score >= 8.5:
        return "Low"
    if score >= 6.5:
        return "Medium"
    return "High"

def score_yes_no_answers(answers: Dict[str, str]) -> float:
    """Simple scoring: Yes = 1, No = 0, Unknown = 0.5; average * 10."""
    if not answers:
        return 5.0
    total = 0.0
    for v in answers.values():
        v = (v or "").strip().lower()
        if v in ("yes", "y", "true", "enabled"):
            total += 1.0
        elif v in ("no", "n", "false", "disabled"):
            total += 0.0
        else:
            total += 0.5
    return round((total / len(answers)) * 10.0, 2)

def merge_text_blocks(items):
    return [i for i in items if i]
