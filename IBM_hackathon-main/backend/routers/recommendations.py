from fastapi import APIRouter, HTTPException, Query
from database import db
from services.recommendation_service import recommend_next, get_resources_for
from schemas import ChatRequest
from chatbot import chat as chatbot_reply
import urllib.parse

router = APIRouter(tags=["recommendations"])


@router.get("/recommendations/{student_id}")
def get_recommendation(student_id: str):
    student = db["students"].get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return recommend_next(student)


@router.get("/resources/{concept}")
def get_resources(concept: str, style: str = Query("visual-first")):
    concept_decoded = urllib.parse.unquote(concept)
    from chatbot import RESOURCES
    if concept_decoded not in RESOURCES:
        raise HTTPException(404, f"No resources for: {concept_decoded}")
    resources = get_resources_for(concept_decoded, style)
    return {"concept": concept_decoded, "style": style, "resources": resources}


@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    student = db["students"].get(req.student_id) if req.student_id else None
    return chatbot_reply(req.message, student)
