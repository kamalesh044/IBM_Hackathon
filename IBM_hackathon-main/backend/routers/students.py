from fastapi import APIRouter, HTTPException
from database import db
from services.risk_service import predict_risk, current_concept
from services.recommendation_service import recommend_next
from services.mastery_service import update_mastery_from_quiz, append_attempt, refresh_learning_style
from services.intervention_service import auto_schedule
from services.root_cause_service import trace_root_cause
from schemas import QuizSubmitRequest
from utils.helpers import student_summary
from concept_graph import CONCEPT_GRAPH, CONCEPT_ORDER
from config import settings

router = APIRouter(prefix="/students", tags=["students"])


@router.get("")
def list_students():
    result = []
    for s in db["students"].values():
        cc   = current_concept(s)
        pred = predict_risk(s, cc)
        rec  = recommend_next(s)
        result.append({
            **student_summary(s),
            "current_concept":  cc,
            "risk_probability": pred["risk_probability"],
            "risk_label":       pred["risk_label"],
            "risk_emoji":       pred["risk_emoji"],
            "explanation":      pred["explanation"],
            "root_cause_concept": pred["root_cause_concept"],
            "recommendation":   rec,
        })
    return result


@router.get("/{student_id}")
def get_student(student_id: str):
    student = db["students"].get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    cc   = current_concept(student)
    pred = predict_risk(student, cc)
    rec  = recommend_next(student)
    interventions = [i for i in db["intervention_logs"].values() if i["student_id"] == student_id]
    return {
        **student,
        "current_concept":    cc,
        "prediction":         pred,
        "recommendation":     rec,
        "intervention_history": interventions,
    }


@router.post("/{student_id}/quiz")
def submit_quiz(student_id: str, req: QuizSubmitRequest):
    student = db["students"].get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    update_mastery_from_quiz(student, req.concept, req.score)
    append_attempt(student, req.concept, req.dict())
    refresh_learning_style(student)

    # Predict on next concept downstream
    prereqs_next = [c for c in CONCEPT_ORDER if req.concept in CONCEPT_GRAPH[c]["prerequisites"]]
    predict_concept = prereqs_next[0] if prereqs_next else req.concept
    prediction = predict_risk(student, predict_concept)

    notif = None
    if prediction["risk_probability"] >= settings.intervention_risk_trigger:
        notif = auto_schedule(
            student_id,
            predict_concept,
            prediction["risk_probability"],
            prediction["explanation"],
            prediction["root_cause_concept"],
        )
    return {
        "updated_mastery":      student["mastery_scores"],
        "prediction":           prediction,
        "notification_created": notif is not None,
        "notification":         notif,
    }
