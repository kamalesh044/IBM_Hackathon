"""services/recommendation_service.py — Learning path recommendation."""
from __future__ import annotations
from ml.models.recommendation_model import get_recommendation_model
from chatbot import RESOURCES


def recommend_next(student: dict) -> dict:
    return get_recommendation_model().recommend(student)


def get_resources_for(concept: str, style: str) -> list:
    """Return resources for concept+style, falling back to visual."""
    style_key = style
    if "example" in style:
        style_key = "example-first"
    elif "practice" in style:
        style_key = "practice-first"
    else:
        style_key = "visual"
    res = RESOURCES.get(concept, {})
    return res.get(style_key, res.get("visual", []))
