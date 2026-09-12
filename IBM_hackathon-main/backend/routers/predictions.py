from fastapi import APIRouter, HTTPException
from database import db
from services.risk_service import predict_risk, current_concept
from schemas import PredictRequest
from concept_graph import CONCEPT_GRAPH

router = APIRouter(prefix="/predict", tags=["predictions"])


@router.post("")
def predict(req: PredictRequest):
    student = db["students"].get(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    if req.concept not in CONCEPT_GRAPH:
        raise HTTPException(400, "Unknown concept")
    return predict_risk(student, req.concept)
