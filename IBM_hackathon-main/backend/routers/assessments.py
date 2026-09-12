from fastapi import APIRouter
from schemas import QuizSubmitRequest
from database import db
from fastapi import HTTPException
from services.mastery_service import update_mastery_from_quiz, append_attempt, refresh_learning_style
from services.risk_service import predict_risk, current_concept
from services.intervention_service import auto_schedule
from concept_graph import CONCEPT_GRAPH, CONCEPT_ORDER
from config import settings

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("/quiz")
def submit_quiz_assessment(req: QuizSubmitRequest):
    """
    Alternative quiz submission endpoint under /assessments/quiz.
    Identical behaviour to POST /students/{id}/quiz.
    """
    student = db["students"].get(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    update_mastery_from_quiz(student, req.concept, req.score)
    append_attempt(student, req.concept, req.dict())
    refresh_learning_style(student)

    prereqs_next    = [c for c in CONCEPT_ORDER if req.concept in CONCEPT_GRAPH[c]["prerequisites"]]
    predict_concept = prereqs_next[0] if prereqs_next else req.concept
    prediction      = predict_risk(student, predict_concept)

    notif = None
    if prediction["risk_probability"] >= settings.intervention_risk_trigger:
        notif = auto_schedule(
            req.student_id,
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
