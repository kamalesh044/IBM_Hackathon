"""
ml/data_processing/feature_engineering.py

Transforms cleaned interaction data into per-student, per-concept feature vectors
that feed the mastery and risk ML models.
"""
from __future__ import annotations
from utils.constants import FEATURE_NAMES, CLASS_MEDIAN_TIME

try:
    import pandas as pd
    import numpy as np
    _PANDAS = True
except ImportError:
    _PANDAS = False


class FeatureEngineer:
    """
    Aggregates per-student interactions into the 8 model features:

        prereq_score_pct            — average correctness on prerequisite concept (0–100)
        num_attempts                — total attempts on prerequisite
        repeated_error_count        — questions answered wrong more than once
        time_per_q_ratio            — student avg / class median elapsed time
        days_since_last_practice    — recency signal
        sub_concepts_attempted_pct  — breadth of coverage (0–100)
        engagement_score            — % of assigned questions attempted
        consistency_score           — std-dev–based consistency measure (0–100)
    """

    def __init__(self, class_median_time: float = CLASS_MEDIAN_TIME):
        self.class_median_time = class_median_time

    def extract(self, student_df, concept_questions: list[str]) -> dict:
        """
        student_df  : cleaned interactions for ONE student
        concept_questions: list of question_ids belonging to the target concept

        Returns a dict with exactly the keys in FEATURE_NAMES.
        """
        if not _PANDAS:
            raise ImportError("pandas required")

        cdf = student_df[student_df["question_id"].isin(concept_questions)]

        if cdf.empty:
            return {f: 0.0 for f in FEATURE_NAMES}

        prereq_score_pct = float(cdf["correct"].mean() * 100)
        num_attempts     = int(len(cdf))

        # repeated errors: questions answered wrong ≥2 times
        error_counts = cdf[cdf["correct"] == 0].groupby("question_id").size()
        repeated_error_count = int((error_counts >= 2).sum())

        avg_elapsed = float(cdf["elapsed_sec"].mean())
        time_per_q_ratio = avg_elapsed / max(self.class_median_time, 1)

        # recency: days since last interaction
        if "timestamp" in cdf.columns:
            last_ts = cdf["timestamp"].max()
            most_recent = pd.Timestamp.now().timestamp() * 1000
            days_since_last_practice = max(0, (most_recent - last_ts) / 86_400_000)
        else:
            days_since_last_practice = 7.0

        sub_concepts_attempted_pct = min(100.0, len(cdf["question_id"].unique()) / max(len(concept_questions), 1) * 100)

        total_questions = len(student_df)
        engagement_score = min(100.0, len(cdf) / max(total_questions, 1) * 100)

        # consistency: inverse of normalised std-dev of correct per session
        daily = cdf.groupby(cdf["timestamp"] // 86_400_000)["correct"].mean()
        if len(daily) > 1:
            consistency_score = max(0.0, 100.0 - float(daily.std() * 100))
        else:
            consistency_score = 70.0

        return {
            "prereq_score_pct":           prereq_score_pct,
            "num_attempts":               float(num_attempts),
            "repeated_error_count":       float(repeated_error_count),
            "time_per_q_ratio":           time_per_q_ratio,
            "days_since_last_practice":   days_since_last_practice,
            "sub_concepts_attempted_pct": sub_concepts_attempted_pct,
            "engagement_score":           engagement_score,
            "consistency_score":          consistency_score,
        }

    def build_dataset(self, df, concept_question_map: dict) -> "pd.DataFrame":
        """
        Build a full feature matrix from a multi-student interaction DataFrame.

        concept_question_map: {concept_name: [question_id, ...]}
        Returns DataFrame with FEATURE_NAMES columns + student_id + concept.
        """
        if not _PANDAS:
            raise ImportError("pandas required")
        rows = []
        for student_id, sdf in df.groupby("student_id"):
            for concept, qids in concept_question_map.items():
                feats = self.extract(sdf, qids)
                feats["student_id"] = student_id
                feats["concept"]    = concept
                rows.append(feats)
        return pd.DataFrame(rows)
