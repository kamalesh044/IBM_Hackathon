from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import db
from services.mastery_service import get_mastery, bkt_mastery_scores
from utils.constants import CONCEPT_ORDER

router = APIRouter(prefix="/mastery", tags=["mastery"])


@router.get("/{student_id}")
def student_mastery(student_id: str):
    student = db["students"].get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return {
        "student_id":   student_id,
        "mastery":      get_mastery(student_id),
        "bkt_mastery":  bkt_mastery_scores(student),
    }


@router.get("/{student_id}/{concept}")
def concept_mastery(student_id: str, concept: str):
    student = db["students"].get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    if concept not in CONCEPT_ORDER:
        raise HTTPException(400, "Unknown concept")
    return {
        "student_id": student_id,
        "concept":    concept,
        "mastery":    student["mastery_scores"].get(concept, 0),
    }
