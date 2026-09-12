"""utils/helpers.py — Shared utility functions."""
from __future__ import annotations
from utils.constants import RISK_LABELS, RISK_EMOJI


def risk_label(prob: float) -> str:
    if prob < 0.30:
        return "LOW"
    if prob < 0.60:
        return "MEDIUM"
    return "HIGH"


def risk_emoji(prob: float) -> str:
    return RISK_EMOJI[risk_label(prob)]


def current_concept(student: dict, concept_order: list[str]) -> str:
    """Return the highest-index concept the student has attempted (score > 0)."""
    mastery = student.get("mastery_scores", {})
    current = concept_order[0]
    for c in concept_order:
        if c in mastery and mastery[c] > 0:
            current = c
    return current


def student_summary(s: dict) -> dict:
    return {
        "id":               s["id"],
        "name":             s["name"],
        "mastery_scores":   s["mastery_scores"],
        "engagement_score": s.get("engagement_score", 0),
        "consistency_score":s.get("consistency_score", 0),
        "learning_style":   s.get("learning_style", "visual-first"),
        "notes":            s.get("notes", ""),
        "risk_profile":     s.get("risk_profile", "unknown"),
    }
