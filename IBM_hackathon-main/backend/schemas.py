"""
Pydantic request / response schemas.
All request body models are defined here and imported by routers.
"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Requests ───────────────────────────────────────────────────────────────────

class QuizSubmitRequest(BaseModel):
    student_id: str
    concept: str
    score: float = Field(..., ge=0, le=100)
    attempts: int = Field(default=1, ge=1)
    repeated_errors: int = Field(default=0, ge=0)
    avg_time_per_q: float = Field(default=75.0, gt=0)
    sub_concepts_attempted_pct: float = Field(default=80.0, ge=0, le=100)
    activity_type: str = "practice"
    error_tags: List[str] = []


class PredictRequest(BaseModel):
    student_id: str
    concept: str


class NotificationActionRequest(BaseModel):
    status: str          # confirmed | declined | rescheduled
    new_slot: Optional[str] = None


class SessionCompleteRequest(BaseModel):
    notification_id: str


class FollowUpQuizRequest(BaseModel):
    student_id: str
    concept: str
    score: float = Field(..., ge=0, le=100)


class ChatRequest(BaseModel):
    message: str
    student_id: Optional[str] = None


# ── Response helpers ───────────────────────────────────────────────────────────

class RiskPrediction(BaseModel):
    risk_probability: float
    risk_label: str
    risk_emoji: str
    top_contributing_features: List[dict] = []
    explanation: str
    root_cause_concept: str
    features_used: Optional[dict] = None


class RecommendationResponse(BaseModel):
    next_concept: Optional[str]
    learning_style: str
    learning_path: str


class InterventionLog(BaseModel):
    id: str
    student_id: str
    student_name: str
    concept: str
    mentor_id: Optional[str]
    pre_score: float
    post_score: float
    improvement_delta: float
    date: str
