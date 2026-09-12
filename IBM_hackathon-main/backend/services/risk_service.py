"""services/risk_service.py — Risk prediction orchestration."""
from __future__ import annotations
from config import settings
from concept_graph import CONCEPT_GRAPH
from ml.models.risk_model import get_risk_model
from utils.helpers import risk_label, risk_emoji
from utils.constants import CONCEPT_ORDER


def predict_risk(student: dict, concept: str) -> dict:
    """
    Full risk prediction pipeline for a student on a concept.
    Returns the standard prediction dict used by all endpoints.
    """
    model = get_risk_model()

    if not model.loaded:
        mastery = student["mastery_scores"].get(concept, 50)
        prob = max(0.0, min(1.0, (100 - mastery) / 100))
        return {
            "risk_probability":          round(prob, 3),
            "risk_label":                risk_label(prob),
            "risk_emoji":                risk_emoji(prob),
            "top_contributing_features": [],
            "explanation":               f"Heuristic fallback: mastery {mastery}%.",
            "root_cause_concept":        concept,
            "features_used":             {},
        }

    features = model.feature_vector(student, concept, CONCEPT_GRAPH)
    prob, top_features = model.predict(features)

    from services.root_cause_service import trace_root_cause, build_explanation
    root_cause = trace_root_cause(concept, student["mastery_scores"])
    explanation = build_explanation(prob, features, top_features, root_cause, concept, student["mastery_scores"])

    return {
        "risk_probability":          round(prob, 3),
        "risk_label":                risk_label(prob),
        "risk_emoji":                risk_emoji(prob),
        "top_contributing_features": [
            {"feature": f, "importance": round(i, 4)} for f, i in top_features
        ],
        "explanation":    explanation,
        "root_cause_concept": root_cause,
        "features_used":  features,
    }


def current_concept(student: dict) -> str:
    """Return the highest-index concept the student has actively attempted."""
    mastery = student.get("mastery_scores", {})
    current = CONCEPT_ORDER[0]
    for c in CONCEPT_ORDER:
        if c in mastery and mastery[c] > 0:
            current = c
    return current
