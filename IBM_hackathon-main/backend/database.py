"""
In-memory database layer.
Initialised once at import time from seed_data.
All routers import `db` directly — no ORM, no external DB required for the demo.
"""
from __future__ import annotations

import copy
from typing import Any, Dict

from seed_data import (
    INITIAL_INTERVENTION_LOGS,
    INITIAL_NOTIFICATIONS,
    MENTORS,
    STUDENTS,
)

# ── Main store ─────────────────────────────────────────────────────────────────
_student_map: Dict[str, Any] = {s["id"]: s for s in STUDENTS}

db: Dict[str, Any] = {
    "students": {s["id"]: copy.deepcopy(s) for s in STUDENTS},
    "mentors":  {m["id"]: copy.deepcopy(m) for m in MENTORS},
    "notifications": {},
    "intervention_logs": {i["id"]: copy.deepcopy(i) for i in INITIAL_INTERVENTION_LOGS},
    "sessions": {},
}

# Enrich pre-seeded notifications with student_name
for _n in INITIAL_NOTIFICATIONS:
    _enriched = copy.deepcopy(_n)
    _enriched.setdefault(
        "student_name",
        _student_map.get(_n["student_id"], {}).get("name", _n["student_id"]),
    )
    db["notifications"][_n["id"]] = _enriched


def get_student(student_id: str) -> dict | None:
    return db["students"].get(student_id)


def get_mentor(mentor_id: str) -> dict | None:
    return db["mentors"].get(mentor_id)


def all_students() -> list[dict]:
    return list(db["students"].values())


def all_mentors() -> list[dict]:
    return list(db["mentors"].values())


def all_notifications() -> list[dict]:
    return list(db["notifications"].values())


def all_sessions() -> list[dict]:
    return list(db["sessions"].values())


def all_intervention_logs() -> list[dict]:
    return list(db["intervention_logs"].values())
