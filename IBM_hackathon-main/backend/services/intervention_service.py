"""services/intervention_service.py — Mentor notification & session management."""
from __future__ import annotations
import uuid
from datetime import datetime

from config import settings
from database import db
from utils.helpers import risk_label


def auto_schedule(
    student_id: str,
    concept: str,
    risk_prob: float,
    explanation: str,
    root_cause: str,
) -> dict | None:
    """
    Create a mentor notification if risk is HIGH and no pending notification
    already exists for the same student + concept.
    Returns the notification dict or None.
    """
    # Deduplicate
    for n in db["notifications"].values():
        if (n["student_id"] == student_id
                and n["concept"] == concept
                and n["status"] == "pending"):
            return None

    # Find a mentor covering this concept
    mentor = None
    for m in db["mentors"].values():
        if concept in m.get("concept_expertise", []) and m.get("free_slots"):
            mentor = m
            break
    if not mentor:
        return None

    proposed_slot = mentor["free_slots"][0]
    student = db["students"].get(student_id, {})

    notif_id = "n" + str(uuid.uuid4())[:8]
    notif = {
        "id":                    notif_id,
        "mentor_id":             mentor["id"],
        "student_id":            student_id,
        "student_name":          student.get("name", student_id),
        "concept":               concept,
        "risk_score":            round(risk_prob * 100),
        "risk_label":            risk_label(risk_prob),
        "root_cause_concept":    root_cause,
        "root_cause_explanation": explanation,
        "proposed_slot":         proposed_slot,
        "status":                "pending",
        "created_at":            datetime.utcnow().isoformat(),
    }
    db["notifications"][notif_id] = notif
    return notif


def confirm_notification(notif_id: str, status: str, new_slot: str | None = None) -> dict:
    """Update notification status and create a session if confirmed."""
    notif = db["notifications"][notif_id]
    notif["status"] = status
    if new_slot:
        notif["proposed_slot"] = new_slot
    notif["updated_at"] = datetime.utcnow().isoformat()

    if status == "confirmed":
        session_id = "sess_" + notif_id
        db["sessions"][session_id] = {
            "id":              session_id,
            "notification_id": notif_id,
            "mentor_id":       notif["mentor_id"],
            "student_id":      notif["student_id"],
            "concept":         notif["concept"],
            "scheduled_slot":  notif["proposed_slot"],
            "status":          "upcoming",
            "created_at":      datetime.utcnow().isoformat(),
        }
    return notif


def complete_session(session_id: str) -> dict:
    session = db["sessions"][session_id]
    session["status"] = "completed"
    session["completed_at"] = datetime.utcnow().isoformat()
    return session


def log_followup(student_id: str, concept: str, post_score: float) -> dict:
    """Log a post-intervention quiz result and update student mastery."""
    student = db["students"].get(student_id, {})
    pre_score = student.get("mastery_scores", {}).get(concept, 0)

    # Find mentor from a completed session
    mentor_id = None
    for sess in db["sessions"].values():
        if (sess["student_id"] == student_id
                and sess["concept"] == concept
                and sess["status"] == "completed"):
            mentor_id = sess["mentor_id"]
            break

    student.setdefault("mastery_scores", {})[concept] = round(post_score, 1)
    delta = round(post_score - pre_score, 1)

    log_id = "i" + str(uuid.uuid4())[:8]
    log = {
        "id":                log_id,
        "student_id":        student_id,
        "student_name":      student.get("name", student_id),
        "concept":           concept,
        "mentor_id":         mentor_id,
        "pre_score":         round(pre_score, 1),
        "post_score":        round(post_score, 1),
        "improvement_delta": delta,
        "date":              datetime.utcnow().isoformat(),
    }
    db["intervention_logs"][log_id] = log
    return log


def intervention_summary() -> dict:
    logs = list(db["intervention_logs"].values())
    if not logs:
        return {"total_sessions": 0, "avg_improvement": 0, "logs": []}
    avg = round(sum(l["improvement_delta"] for l in logs) / len(logs), 1)
    return {"total_sessions": len(logs), "avg_improvement": avg, "logs": logs}
