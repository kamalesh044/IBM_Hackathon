"""
AI Learning Intelligence Platform — FastAPI entry point (v2)

Structured backend:
    routers/     — HTTP layer (one file per domain)
    services/    — business logic
    ml/          — ML models, data pipeline
    utils/       — shared constants and helpers
    database.py  — in-memory store
    schemas.py   — Pydantic request/response models
    config.py    — application settings
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from concept_graph import CONCEPT_GRAPH, CONCEPT_ORDER

# ── Routers ────────────────────────────────────────────────────────────────────
from routers.students       import router as students_router
from routers.predictions    import router as predictions_router
from routers.interventions  import router as interventions_router
from routers.faculty        import router as faculty_router
from routers.analytics      import router as analytics_router
from routers.mastery        import router as mastery_router
from routers.recommendations import router as recommendations_router
from routers.assessments    import router as assessments_router

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=(
        "Predictive Concept-Readiness · Root-Cause Analysis · "
        "Personalized Learning · Mentor Intervention"
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount all routers ──────────────────────────────────────────────────────────
app.include_router(students_router)
app.include_router(predictions_router)
app.include_router(interventions_router)
app.include_router(faculty_router)
app.include_router(analytics_router)
app.include_router(mastery_router)
app.include_router(recommendations_router)
app.include_router(assessments_router)


# ── Health / meta ──────────────────────────────────────────────────────────────
@app.get("/", tags=["health"])
def health():
    return {
        "status":  "ok",
        "service": settings.app_title,
        "version": settings.app_version,
    }


@app.get("/concepts", tags=["concepts"])
def get_concepts():
    return {"concepts": CONCEPT_GRAPH, "order": CONCEPT_ORDER}


# ── Mentor list (kept at top level for backward compatibility) ──────────────────
from database import db

@app.get("/mentors", tags=["mentors"])
def list_mentors():
    return list(db["mentors"].values())


@app.get("/mentors/{mentor_id}", tags=["mentors"])
def get_mentor(mentor_id: str):
    from fastapi import HTTPException
    m = db["mentors"].get(mentor_id)
    if not m:
        raise HTTPException(404, "Mentor not found")
    sessions = [s for s in db["sessions"].values() if s.get("mentor_id") == mentor_id]
    pending  = [n for n in db["notifications"].values()
                if n.get("mentor_id") == mentor_id and n.get("status") == "pending"]
    return {**m, "sessions": sessions, "pending_notification_count": len(pending)}
