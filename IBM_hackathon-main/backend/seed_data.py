"""
Synthetic seed data for demo: 7 students + 2 mentors.
Designed to cover:
  - 2 low-risk (on track)
  - 2 medium-risk
  - 2 high-risk
  - 1 "high marks but shallow understanding"
  - 1 "low marks but conceptually sound" (overlaps with above set)
"""

import json
from datetime import datetime, timedelta

BASE_DATE = datetime(2024, 6, 1)


def d(days_offset: int) -> str:
    return (BASE_DATE + timedelta(days=days_offset)).isoformat()


STUDENTS = [
    # ---- LOW RISK ----
    {
        "id": "s001",
        "name": "Aisha Patel",
        "risk_profile": "low",
        "learning_style": "practice-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 92,
            "Recursion": 88,
            "Tree Traversal": 81,
            "Binary Search Trees": 75,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 90, "attempts": 1,
             "repeated_errors": 0, "avg_time_per_q": 42, "last_practice_days_ago": 3,
             "sub_concepts_attempted_pct": 100, "activity_type": "practice",
             "error_tags": []},
            {"concept": "Recursion", "score": 85, "attempts": 2,
             "repeated_errors": 0, "avg_time_per_q": 55, "last_practice_days_ago": 5,
             "sub_concepts_attempted_pct": 100, "activity_type": "practice",
             "error_tags": []},
            {"concept": "Tree Traversal", "score": 80, "attempts": 2,
             "repeated_errors": 1, "avg_time_per_q": 60, "last_practice_days_ago": 2,
             "sub_concepts_attempted_pct": 80, "activity_type": "practice",
             "error_tags": ["post-order confusion"]},
        ],
        "engagement_score": 92,
        "consistency_score": 90,
        "notes": "Consistently strong. Self-sufficient learner.",
    },
    {
        "id": "s002",
        "name": "Carlos Mendez",
        "risk_profile": "low",
        "learning_style": "example-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 95,
            "Recursion": 82,
            "Tree Traversal": 78,
            "Binary Search Trees": 40,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 95, "attempts": 1,
             "repeated_errors": 0, "avg_time_per_q": 38, "last_practice_days_ago": 7,
             "sub_concepts_attempted_pct": 100, "activity_type": "worked_example",
             "error_tags": []},
            {"concept": "Recursion", "score": 80, "attempts": 2,
             "repeated_errors": 1, "avg_time_per_q": 62, "last_practice_days_ago": 6,
             "sub_concepts_attempted_pct": 80, "activity_type": "worked_example",
             "error_tags": ["base case"]},
            {"concept": "Tree Traversal", "score": 75, "attempts": 3,
             "repeated_errors": 1, "avg_time_per_q": 70, "last_practice_days_ago": 4,
             "sub_concepts_attempted_pct": 60, "activity_type": "worked_example",
             "error_tags": ["BFS order"]},
        ],
        "engagement_score": 85,
        "consistency_score": 80,
        "notes": "Good fundamentals. BST still fresh.",
    },
    # ---- MEDIUM RISK ----
    {
        "id": "s003",
        "name": "Priya Singh",
        "risk_profile": "medium",
        "learning_style": "visual-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 70,
            "Recursion": 52,
            "Tree Traversal": 38,
            "Binary Search Trees": 20,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 70, "attempts": 3,
             "repeated_errors": 1, "avg_time_per_q": 78, "last_practice_days_ago": 10,
             "sub_concepts_attempted_pct": 80, "activity_type": "practice",
             "error_tags": ["pointer manipulation"]},
            {"concept": "Recursion", "score": 50, "attempts": 4,
             "repeated_errors": 2, "avg_time_per_q": 92, "last_practice_days_ago": 8,
             "sub_concepts_attempted_pct": 60, "activity_type": "practice",
             "error_tags": ["base case", "call stack"]},
            {"concept": "Tree Traversal", "score": 35, "attempts": 3,
             "repeated_errors": 2, "avg_time_per_q": 110, "last_practice_days_ago": 5,
             "sub_concepts_attempted_pct": 40, "activity_type": "practice",
             "error_tags": ["in-order", "DFS"]},
        ],
        "engagement_score": 60,
        "consistency_score": 55,
        "notes": "Needs visual aids. Struggles with abstract recursion.",
    },
    {
        "id": "s004",
        "name": "Jordan Lee",
        "risk_profile": "medium",
        "learning_style": "practice-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 65,
            "Recursion": 55,
            "Tree Traversal": 45,
            "Binary Search Trees": 15,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 65, "attempts": 4,
             "repeated_errors": 2, "avg_time_per_q": 85, "last_practice_days_ago": 12,
             "sub_concepts_attempted_pct": 60, "activity_type": "practice",
             "error_tags": ["two-pointer"]},
            {"concept": "Recursion", "score": 55, "attempts": 5,
             "repeated_errors": 2, "avg_time_per_q": 95, "last_practice_days_ago": 9,
             "sub_concepts_attempted_pct": 60, "activity_type": "practice",
             "error_tags": ["recursive case", "memoization"]},
            {"concept": "Tree Traversal", "score": 40, "attempts": 4,
             "repeated_errors": 3, "avg_time_per_q": 105, "last_practice_days_ago": 6,
             "sub_concepts_attempted_pct": 40, "activity_type": "practice",
             "error_tags": ["pre-order", "BFS"]},
        ],
        "engagement_score": 55,
        "consistency_score": 50,
        "notes": "Persistent but needs structured support.",
    },
    # ---- HIGH RISK ----
    {
        "id": "s005",
        "name": "Fatima Al-Rashid",
        "risk_profile": "high",
        "learning_style": "visual-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 40,
            "Recursion": 28,
            "Tree Traversal": 18,
            "Binary Search Trees": 5,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 38, "attempts": 5,
             "repeated_errors": 3, "avg_time_per_q": 130, "last_practice_days_ago": 14,
             "sub_concepts_attempted_pct": 40, "activity_type": "practice",
             "error_tags": ["traversal", "pointer manipulation"]},
            {"concept": "Recursion", "score": 25, "attempts": 6,
             "repeated_errors": 4, "avg_time_per_q": 150, "last_practice_days_ago": 10,
             "sub_concepts_attempted_pct": 40, "activity_type": "practice",
             "error_tags": ["base case", "call stack", "infinite loop"]},
            {"concept": "Tree Traversal", "score": 18, "attempts": 4,
             "repeated_errors": 3, "avg_time_per_q": 160, "last_practice_days_ago": 7,
             "sub_concepts_attempted_pct": 20, "activity_type": "practice",
             "error_tags": ["all traversal types"]},
        ],
        "engagement_score": 35,
        "consistency_score": 30,
        "notes": "Fundamental gaps across all concepts. Needs immediate intervention.",
    },
    # ---- HIGH MARKS BUT SHALLOW UNDERSTANDING ----
    {
        "id": "s006",
        "name": "Wei Zhang",
        "risk_profile": "medium",
        "learning_style": "example-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 88,
            "Recursion": 45,
            "Tree Traversal": 35,
            "Binary Search Trees": 10,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 92, "attempts": 1,
             "repeated_errors": 0, "avg_time_per_q": 35, "last_practice_days_ago": 3,
             "sub_concepts_attempted_pct": 60, "activity_type": "worked_example",
             "error_tags": []},
            {"concept": "Recursion", "score": 42, "attempts": 6,
             "repeated_errors": 3, "avg_time_per_q": 120, "last_practice_days_ago": 8,
             "sub_concepts_attempted_pct": 40, "activity_type": "worked_example",
             "error_tags": ["base case", "recursive case"]},
            {"concept": "Tree Traversal", "score": 32, "attempts": 5,
             "repeated_errors": 3, "avg_time_per_q": 135, "last_practice_days_ago": 5,
             "sub_concepts_attempted_pct": 40, "activity_type": "worked_example",
             "error_tags": ["post-order", "DFS"]},
        ],
        "engagement_score": 70,
        "consistency_score": 50,
        "notes": "High marks on easy sections; hits a wall at Recursion. Shallow foundation.",
    },
    # ---- LOW MARKS BUT CONCEPTUALLY SOUND ----
    {
        "id": "s007",
        "name": "Rohan Kumar",
        "risk_profile": "low",
        "learning_style": "visual-first",
        "mastery_scores": {
            "Arrays/Linked Lists": 62,
            "Recursion": 68,
            "Tree Traversal": 65,
            "Binary Search Trees": 58,
        },
        "attempt_history": [
            {"concept": "Arrays/Linked Lists", "score": 60, "attempts": 4,
             "repeated_errors": 1, "avg_time_per_q": 90, "last_practice_days_ago": 4,
             "sub_concepts_attempted_pct": 100, "activity_type": "visual",
             "error_tags": ["timing issues"]},
            {"concept": "Recursion", "score": 65, "attempts": 3,
             "repeated_errors": 1, "avg_time_per_q": 85, "last_practice_days_ago": 3,
             "sub_concepts_attempted_pct": 100, "activity_type": "visual",
             "error_tags": ["speed"]},
            {"concept": "Tree Traversal", "score": 62, "attempts": 4,
             "repeated_errors": 1, "avg_time_per_q": 95, "last_practice_days_ago": 2,
             "sub_concepts_attempted_pct": 80, "activity_type": "visual",
             "error_tags": ["speed under pressure"]},
        ],
        "engagement_score": 78,
        "consistency_score": 85,
        "notes": "Conceptually solid. Test anxiety affects scores. Broad coverage.",
    },
]

MENTORS = [
    {
        "id": "m001",
        "name": "Dr. Sarah Chen",
        "concept_expertise": [
            "Arrays/Linked Lists",
            "Recursion",
            "Tree Traversal",
        ],
        "free_slots": [
            d(2) + "T10:00:00",
            d(2) + "T14:00:00",
            d(3) + "T09:00:00",
            d(4) + "T11:00:00",
            d(5) + "T15:00:00",
        ],
        "bio": "10 years teaching DSA. Specialises in breaking down recursive thinking.",
    },
    {
        "id": "m002",
        "name": "Prof. Mark Thompson",
        "concept_expertise": [
            "Recursion",
            "Tree Traversal",
            "Binary Search Trees",
        ],
        "free_slots": [
            d(1) + "T13:00:00",
            d(3) + "T10:00:00",
            d(3) + "T16:00:00",
            d(6) + "T10:00:00",
            d(7) + "T14:00:00",
        ],
        "bio": "Research background in algorithm analysis. Tree structures specialist.",
    },
]

# Pre-seeded notifications (2 pending at load time)
INITIAL_NOTIFICATIONS = [
    {
        "id": "n001",
        "mentor_id": "m001",
        "student_id": "s005",
        "concept": "Recursion",
        "risk_score": 82,
        "risk_label": "HIGH",
        "root_cause_concept": "Arrays/Linked Lists",
        "root_cause_explanation": (
            "Fatima's difficulty with Recursion traces back to a gap in "
            "Arrays/Linked Lists (mastery: 40%), not the topic itself."
        ),
        "proposed_slot": d(2) + "T10:00:00",
        "status": "pending",
        "created_at": d(0),
    },
    {
        "id": "n002",
        "mentor_id": "m002",
        "student_id": "s006",
        "concept": "Tree Traversal",
        "risk_score": 75,
        "risk_label": "HIGH",
        "root_cause_concept": "Recursion",
        "root_cause_explanation": (
            "Wei's difficulty with Tree Traversal traces back to a gap in "
            "Recursion (mastery: 45%), not the topic itself."
        ),
        "proposed_slot": d(3) + "T10:00:00",
        "status": "pending",
        "created_at": d(0),
    },
]

# Pre-seeded intervention logs (1 completed showing improvement)
INITIAL_INTERVENTION_LOGS = [
    {
        "id": "i001",
        "student_id": "s003",
        "concept": "Recursion",
        "mentor_id": "m001",
        "pre_score": 38,
        "post_score": 67,
        "improvement_delta": 29,
        "date": d(-7),
        "session_notes": "Focused on base-case patterns and call-stack visualisation.",
    },
    {
        "id": "i002",
        "student_id": "s004",
        "concept": "Arrays/Linked Lists",
        "mentor_id": "m001",
        "pre_score": 45,
        "post_score": 72,
        "improvement_delta": 27,
        "date": d(-3),
        "session_notes": "Two-pointer and traversal exercises with worked examples.",
    },
]
