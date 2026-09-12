from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db

router = APIRouter(prefix="/mentors", tags=["mentors"])


@router.get("")
def list_mentors():
    return list(db["mentors"].values())


@router.get("/{mentor_id}")
def get_mentor(mentor_id: str):
    m = db["mentors"].get(mentor_id)
    if not m:
        raise HTTPException(404, "Mentor not found")
    sessions = [s for s in db["sessions"].values() if s.get("mentor_id") == mentor_id]
    pending  = [n for n in db["notifications"].values()
                if n.get("mentor_id") == mentor_id and n.get("status") == "pending"]
    return {**m, "sessions": sessions, "pending_notification_count": len(pending)}
