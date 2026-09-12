"""
Application configuration — loaded once at startup.
All tuneable constants live here so nothing is hard-coded in business logic.
"""
from __future__ import annotations
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "AI Learning Intelligence Platform"
    app_version: str = "2.0.0"

    # ML model paths (relative to the backend/ directory)
    model_dir: str = "ml/saved_models"
    readiness_model_file: str = "readiness_model.joblib"
    feature_names_file: str = "feature_names.json"

    # Risk thresholds
    risk_low_threshold: float = 0.30
    risk_high_threshold: float = 0.60

    # Mastery thresholds
    mastery_target: float = 80.0       # % — considered "mastered"
    mastery_prereq_min: float = 60.0   # % — prerequisite gate
    mastery_struggle_max: float = 70.0 # % — shown in struggle analysis

    # Intervention
    intervention_risk_trigger: float = 0.60  # auto-schedule above this

    # Quiz rolling-average weights
    quiz_new_weight: float = 0.40
    quiz_old_weight: float = 0.60

    # Class median time per question (seconds) — used for time_ratio feature
    class_median_time: float = 75.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
