"""utils/constants.py — Domain constants shared across the codebase."""

CONCEPT_ORDER = [
    "Arrays/Linked Lists",
    "Recursion",
    "Tree Traversal",
    "Binary Search Trees",
]

RISK_LABELS = {
    "LOW":    (0.00, 0.30),
    "MEDIUM": (0.30, 0.60),
    "HIGH":   (0.60, 1.01),
}

RISK_EMOJI = {
    "LOW":    "🟢",
    "MEDIUM": "🟡",
    "HIGH":   "🔴",
}

LEARNING_STYLES = ["visual-first", "example-first", "practice-first"]

ACTIVITY_TYPES = ["practice", "worked_example", "visual", "quiz"]

MASTERY_TARGET      = 80.0   # % — concept considered mastered
MASTERY_PREREQ_MIN  = 60.0   # % — prerequisite gate
MASTERY_STRUGGLE_MAX = 70.0  # % — shown in struggle analysis

CLASS_MEDIAN_TIME   = 75.0   # seconds per question

FEATURE_NAMES = [
    "prereq_score_pct",
    "num_attempts",
    "repeated_error_count",
    "time_per_q_ratio",
    "days_since_last_practice",
    "sub_concepts_attempted_pct",
    "engagement_score",
    "consistency_score",
]
