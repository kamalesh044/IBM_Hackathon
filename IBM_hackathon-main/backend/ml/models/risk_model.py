"""
ml/models/risk_model.py

RandomForest-based at-risk prediction model.
Wraps the trained joblib model and exposes a clean predict() interface.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Tuple

import joblib
import numpy as np

try:
    import pandas as pd
    _PANDAS = True
except ImportError:
    _PANDAS = False

from utils.constants import FEATURE_NAMES, CLASS_MEDIAN_TIME


class RiskModel:
    """
    Loads the pre-trained RandomForestClassifier and provides predict().

    Model lives at: ml/saved_models/readiness_model.joblib
    Features:       ml/saved_models/feature_names.json
    """

    def __init__(self, model_dir: str = "ml/saved_models"):
        self._model     = None
        self._features: List[str] = FEATURE_NAMES
        self._model_dir = Path(model_dir)
        self._load()

    def _load(self):
        model_path   = self._model_dir / "readiness_model.joblib"
        feature_path = self._model_dir / "feature_names.json"
        try:
            self._model = joblib.load(model_path)
            if feature_path.exists():
                with open(feature_path) as f:
                    self._features = json.load(f)
            print(f"[RiskModel] Loaded from {model_path}")
        except FileNotFoundError:
            print(f"[RiskModel] Model not found at {model_path}. Using heuristic fallback.")

    @property
    def loaded(self) -> bool:
        return self._model is not None

    def predict(self, features: dict) -> Tuple[float, List[Tuple[str, float]]]:
        """
        Returns (risk_probability, top_features).
        top_features: [(feature_name, importance), ...]  sorted descending.
        """
        if not self.loaded:
            # Heuristic fallback
            prereq = features.get("prereq_score_pct", 50)
            prob   = max(0.0, min(1.0, (100 - prereq) / 100))
            return prob, []

        if not _PANDAS:
            raise ImportError("pandas required")

        X = pd.DataFrame(
            [[features.get(f, 0.0) for f in self._features]],
            columns=self._features,
        )
        prob = float(self._model.predict_proba(X)[0][1])

        importances = self._model.feature_importances_
        top = sorted(zip(self._features, importances), key=lambda x: -x[1])[:4]
        return prob, list(top)

    def feature_vector(self, student: dict, concept: str, concept_graph: dict) -> dict:
        """
        Build the 8-feature vector for a student on a given concept,
        pulling data from attempt_history.
        """
        prereqs = concept_graph.get(concept, {}).get("prerequisites", [])
        prereq_concept = prereqs[0] if prereqs else concept

        history = [
            a for a in student.get("attempt_history", [])
            if a.get("concept") == prereq_concept
        ]
        latest = history[-1] if history else {}

        prereq_score = latest.get("score", student["mastery_scores"].get(prereq_concept, 50))
        num_attempts = latest.get("attempts", 3)
        repeated_errors = latest.get("repeated_errors", 1)
        avg_time = latest.get("avg_time_per_q", CLASS_MEDIAN_TIME)
        time_ratio = avg_time / CLASS_MEDIAN_TIME
        days_since = latest.get("last_practice_days_ago", 7)
        sub_pct = latest.get("sub_concepts_attempted_pct", 60)
        engagement = student.get("engagement_score", 70)
        consistency = student.get("consistency_score", 70)

        return {
            "prereq_score_pct":           prereq_score,
            "num_attempts":               num_attempts,
            "repeated_error_count":       repeated_errors,
            "time_per_q_ratio":           time_ratio,
            "days_since_last_practice":   days_since,
            "sub_concepts_attempted_pct": sub_pct,
            "engagement_score":           engagement,
            "consistency_score":          consistency,
        }


# Module-level singleton — loaded once when the app starts
_risk_model_instance: RiskModel | None = None


def get_risk_model() -> RiskModel:
    global _risk_model_instance
    if _risk_model_instance is None:
        _risk_model_instance = RiskModel()
    return _risk_model_instance
