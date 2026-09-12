"""
Domain model helpers — thin wrappers that read/write the in-memory db dicts.
Not SQLAlchemy ORM models — just typed helpers for clarity.
"""
from __future__ import annotations
from typing import Any


class Student:
    """Read-only view over a student dict."""
    def __init__(self, data: dict):
        self._d = data

    @property
    def id(self) -> str:
        return self._d["id"]

    @property
    def name(self) -> str:
        return self._d["name"]

    @property
    def mastery_scores(self) -> dict[str, float]:
        return self._d.get("mastery_scores", {})

    @property
    def attempt_history(self) -> list[dict]:
        return self._d.get("attempt_history", [])

    @property
    def learning_style(self) -> str:
        return self._d.get("learning_style", "visual-first")

    @property
    def engagement_score(self) -> float:
        return self._d.get("engagement_score", 70)

    @property
    def consistency_score(self) -> float:
        return self._d.get("consistency_score", 70)

    def to_dict(self) -> dict:
        return self._d


class Notification:
    """Read-only view over a notification dict."""
    def __init__(self, data: dict):
        self._d = data

    @property
    def id(self) -> str:
        return self._d["id"]

    @property
    def status(self) -> str:
        return self._d.get("status", "pending")

    def to_dict(self) -> dict:
        return self._d
