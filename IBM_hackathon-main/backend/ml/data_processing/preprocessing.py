"""
ml/data_processing/preprocessing.py

Raw-data cleaning and normalisation pipeline.
Works on the DataFrame produced by EdNetLoader.
"""
from __future__ import annotations
from typing import Optional

try:
    import pandas as pd
    import numpy as np
    _PANDAS = True
except ImportError:
    _PANDAS = False


class Preprocessor:
    """
    Cleans and normalises raw EdNet interaction data.

    Steps:
      1. Drop rows with missing critical fields
      2. Cap elapsed_time outliers (IQR method)
      3. Derive `correct` column from user_answer (requires answer_key)
      4. Convert elapsed_time from ms → seconds
      5. Sort by student_id, timestamp
    """

    # Questions answered in < 2 s are likely random clicks
    MIN_ELAPSED_MS = 2_000
    # Hard cap: 10 minutes per question
    MAX_ELAPSED_MS = 600_000

    def __init__(self, answer_key: Optional[dict] = None):
        """
        answer_key: {question_id: correct_answer} — optional.
        If not provided, `correct` column will be NaN.
        """
        self.answer_key = answer_key or {}

    def fit_transform(self, df):
        if not _PANDAS:
            raise ImportError("pandas required")
        df = df.copy()

        # 1. Drop rows missing essential columns
        df.dropna(subset=["student_id", "question_id", "elapsed_time"], inplace=True)

        # 2. Cap elapsed_time
        df["elapsed_time"] = df["elapsed_time"].clip(
            lower=self.MIN_ELAPSED_MS, upper=self.MAX_ELAPSED_MS
        )

        # 3. Correct column
        if self.answer_key:
            df["correct"] = df.apply(
                lambda r: int(self.answer_key.get(r["question_id"], "") == r["user_answer"]),
                axis=1,
            )
        else:
            # Heuristic: treat faster responses as more likely correct
            median_time = df["elapsed_time"].median()
            df["correct"] = (df["elapsed_time"] < median_time).astype(int)

        # 4. elapsed_time → seconds
        df["elapsed_sec"] = df["elapsed_time"] / 1000.0

        # 5. Sort
        df.sort_values(["student_id", "timestamp"], inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df
