"""
ml/data_processing/ednet_loader.py

EdNet dataset loader.
EdNet (https://github.com/riiid/ednet) is the flagship dataset for this project.
It contains 131M+ interactions from 784K students.

Usage (when the raw CSV files are placed in data/raw/ednet/):
    from ml.data_processing.ednet_loader import EdNetLoader
    loader = EdNetLoader("data/raw/ednet")
    df = loader.load_kt1(student_limit=5000)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

try:
    import pandas as pd
    _PANDAS = True
except ImportError:
    _PANDAS = False


class EdNetLoader:
    """
    Loads and parses EdNet KT1 interaction files.

    EdNet KT1 schema (per-row):
        timestamp       — unix ms
        solving_id      — question bundle id
        question_id     — specific question (e.g. q123)
        user_answer     — student's answer
        elapsed_time    — ms spent on question
    """

    KT1_DIR = "KT1"

    def __init__(self, root_dir: str = "data/raw/ednet"):
        self.root = Path(root_dir)

    def _kt1_path(self) -> Path:
        return self.root / self.KT1_DIR

    def load_kt1(
        self,
        student_limit: Optional[int] = None,
        min_interactions: int = 10,
    ):
        """
        Load EdNet KT1 interactions.
        Returns a combined DataFrame with column `student_id` added.

        Falls back to a minimal synthetic sample if files are not present
        (so the backend boots without the raw data).
        """
        if not _PANDAS:
            raise ImportError("pandas is required: pip install pandas")

        kt1 = self._kt1_path()
        if not kt1.exists():
            print(f"[EdNetLoader] {kt1} not found — returning synthetic sample.")
            return self._synthetic_sample()

        files = sorted(kt1.glob("u*.csv"))
        if student_limit:
            files = files[:student_limit]

        frames = []
        for f in files:
            df = pd.read_csv(f, header=None,
                             names=["timestamp","solving_id","question_id",
                                    "user_answer","elapsed_time"])
            df["student_id"] = f.stem          # e.g. "u12345"
            if len(df) >= min_interactions:
                frames.append(df)

        if not frames:
            print("[EdNetLoader] No valid files found — returning synthetic sample.")
            return self._synthetic_sample()

        combined = pd.concat(frames, ignore_index=True)
        combined["timestamp"] = pd.to_numeric(combined["timestamp"], errors="coerce")
        combined.sort_values(["student_id", "timestamp"], inplace=True)
        return combined

    @staticmethod
    def _synthetic_sample():
        """Returns a minimal synthetic DataFrame matching KT1 schema."""
        import pandas as pd, numpy as np, random
        random.seed(42); np.random.seed(42)
        rows = []
        for sid in range(1, 51):
            for q in range(30):
                rows.append({
                    "timestamp": 1_600_000_000_000 + q * 60_000,
                    "solving_id": f"b{random.randint(1,100)}",
                    "question_id": f"q{random.randint(1,1000)}",
                    "user_answer": random.choice(["a","b","c","d"]),
                    "elapsed_time": random.randint(5000, 180_000),
                    "student_id": f"u{sid:05d}",
                })
        return pd.DataFrame(rows)
