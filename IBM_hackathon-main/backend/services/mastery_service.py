"""services/mastery_service.py — Student mastery read/write operations."""
from __future__ import annotations
from datetime import datetime
from config import settings
from database import db
from ml.models.mastery_model import BKTMasteryModel
from ml.models.recommendation_model import get_recommendation_model
from utils.constants import CONCEPT_ORDER


def get_mastery(student_id: str) -> dict:
    student = db["students"].get(student_id)
    if not student:
        return {}
    return student["mastery_scores"]


def update_mastery_from_quiz(student: dict, concept: str, score: float) -> float:
    """
    Rolling-average update: new = old * 0.6 + score * 0.4
    Returns new mastery value.
    """
    existing = student["mastery_scores"].get(concept, 0)
    new_mastery = round(
        existing * settings.quiz_old_weight + score * settings.quiz_new_weight, 1
    )
    student["mastery_scores"][concept] = new_mastery
    return new_mastery


def append_attempt(student: dict, concept: str, payload: dict):
    """Append a quiz attempt to the student's attempt_history."""
    student.setdefault("attempt_history", []).append({
        "concept":                    concept,
        "score":                      payload.get("score", 0),
        "attempts":                   payload.get("attempts", 1),
        "repeated_errors":            payload.get("repeated_errors", 0),
        "avg_time_per_q":             payload.get("avg_time_per_q", 75),
        "last_practice_days_ago":     0,
        "sub_concepts_attempted_pct": payload.get("sub_concepts_attempted_pct", 80),
        "activity_type":              payload.get("activity_type", "practice"),
        "error_tags":                 payload.get("error_tags", []),
        "timestamp":                  datetime.utcnow().isoformat(),
    })


def refresh_learning_style(student: dict):
    """Re-derive and store learning style from latest attempt history."""
    rec = get_recommendation_model()
    student["learning_style"] = rec.derive_style(student.get("attempt_history", []))


def bkt_mastery_scores(student: dict) -> dict:
    """Return BKT-computed mastery for all concepts."""
    history = student.get("attempt_history", [])
    return {
        c: BKTMasteryModel.score_from_attempts(c, history)
        for c in CONCEPT_ORDER
    }
