from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db
from services.intervention_service import confirm_notification
from schemas import NotificationActionRequest

router = APIRouter(tags=["interventions"])


# ── Notifications ──────────────────────────────────────────────────────────────

@router.get("/notifications")
def get_notifications(
    mentor_id: Optional[str] = Query(None),
    status:    Optional[str] = Query(None),
):
    notifs = list(db["notifications"].values())
    if mentor_id:
        notifs = [n for n in notifs if n.get("mentor_id") == mentor_id]
    if status:
        notifs = [n for n in notifs if n.get("status") == status]
    notifs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return notifs


@router.patch("/notifications/{notif_id}")
def update_notification(notif_id: str, req: NotificationActionRequest):
    if notif_id not in db["notifications"]:
        raise HTTPException(404, "Notification not found")
    return confirm_notification(notif_id, req.status, req.new_slot)


# ── Sessions ───────────────────────────────────────────────────────────────────

@router.get("/sessions")
def get_sessions(mentor_id: Optional[str] = Query(None)):
    sessions = list(db["sessions"].values())
    if mentor_id:
        sessions = [s for s in sessions if s.get("mentor_id") == mentor_id]
    return sessions


@router.post("/sessions/{session_id}/complete")
def mark_session_complete(session_id: str):
    if session_id not in db["sessions"]:
        raise HTTPException(404, "Session not found")
    from services.intervention_service import complete_session
    return complete_session(session_id)


# ── Intervention logs ──────────────────────────────────────────────────────────

@router.get("/interventions")
def list_interventions(student_id: Optional[str] = Query(None)):
    logs = list(db["intervention_logs"].values())
    if student_id:
        logs = [l for l in logs if l["student_id"] == student_id]
    return logs


@router.post("/interventions/followup")
def followup_quiz(req_body: dict):
    from schemas import FollowUpQuizRequest
    req = FollowUpQuizRequest(**req_body)
    if req.student_id not in db["students"]:
        raise HTTPException(404, "Student not found")
    from services.intervention_service import log_followup
    return log_followup(req.student_id, req.concept, req.score)


@router.get("/interventions/summary")
def summary():
    from services.intervention_service import intervention_summary
    return intervention_summary()
