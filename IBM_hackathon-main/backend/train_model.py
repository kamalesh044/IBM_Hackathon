"""
Offline ML training script.
Run once:  python train_model.py
Outputs:   model/readiness_model.joblib
           model/feature_names.json
"""

import json
import os
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

random.seed(42)
np.random.seed(42)

# ── Feature columns ───────────────────────────────────────────────────────────
FEATURE_NAMES = [
    "prereq_score_pct",          # 0-100
    "num_attempts",              # 1-10
    "repeated_error_count",      # 0-10
    "time_per_q_ratio",          # actual / class_median  (>1 = slower)
    "days_since_last_practice",  # 0-30
    "sub_concepts_attempted_pct",# 0-100
    "engagement_score",          # 0-100
    "consistency_score",         # 0-100
]


def generate_dataset(n: int = 400) -> pd.DataFrame:
    rows = []
    for _ in range(n):
        prereq_score = random.uniform(10, 100)
        num_attempts = random.randint(1, 10)
        repeated_errors = random.randint(0, 6)
        time_ratio = random.uniform(0.5, 2.5)
        days_since = random.randint(0, 28)
        sub_pct = random.uniform(20, 100)
        engagement = random.uniform(20, 100)
        consistency = random.uniform(20, 100)

        # Rule-derived label: 1 = "at risk"
        at_risk = int(
            prereq_score < 50
            or repeated_errors >= 2
            or time_ratio > 1.6
            or (days_since > 14 and prereq_score < 70)
        )

        rows.append([
            prereq_score, num_attempts, repeated_errors, time_ratio,
            days_since, sub_pct, engagement, consistency, at_risk,
        ])

    df = pd.DataFrame(rows, columns=FEATURE_NAMES + ["label"])
    return df


def main():
    os.makedirs("model", exist_ok=True)

    df = generate_dataset(400)
    X = df[FEATURE_NAMES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced",
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=["on_track", "at_risk"]))

    importances = dict(zip(FEATURE_NAMES, clf.feature_importances_.tolist()))
    print("\n=== Feature Importances ===")
    for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
        print(f"  {feat}: {imp:.4f}")

    joblib.dump(clf, "model/readiness_model.joblib")
    with open("model/feature_names.json", "w") as f:
        json.dump(FEATURE_NAMES, f)

    print("\nModel saved to model/readiness_model.joblib")


if __name__ == "__main__":
    main()
