"""
Personalized Learning-Method Recommendation (rule-based).

Learning style signal is derived from the student's attempt_history:
  - If average score_after_examples > average score_after_practice  → example-first
  - If improvement is mainly driven by repetitions               → practice-first
  - Otherwise (low engagement / visual signals)                  → visual-first

For this prototype, the style is stored directly on the student profile
and derived once from seeded data.
"""

from concept_graph import CONCEPT_GRAPH, CONCEPT_ORDER


LEARNING_PATHS = {
    "example-first": (
        "Short concept video -> Worked example -> 5 practice questions"
    ),
    "practice-first": (
        "Quick concept summary -> Practice problems -> Adaptive difficulty drills"
    ),
    "visual-first": (
        "Visual diagram / animation -> Step-by-step walkthrough -> Guided problems"
    ),
}


def derive_learning_style(attempt_history: list) -> str:
    """
    Derive learning style from attempt history.
    Returns one of: 'example-first', 'practice-first', 'visual-first'.
    """
    if not attempt_history:
        return "visual-first"

    example_scores = [
        a["score"]
        for a in attempt_history
        if a.get("activity_type") == "worked_example"
    ]
    practice_scores = [
        a["score"]
        for a in attempt_history
        if a.get("activity_type") == "practice"
    ]

    avg_example = sum(example_scores) / len(example_scores) if example_scores else 0
    avg_practice = sum(practice_scores) / len(practice_scores) if practice_scores else 0

    if avg_example >= avg_practice and avg_example > 0:
        return "example-first"
    if avg_practice > avg_example:
        return "practice-first"
    return "visual-first"


def recommend_next(student: dict) -> dict:
    """
    Returns:
      {
        "next_concept": str | None,
        "learning_style": str,
        "learning_path": str,
        "root_cause_concept": str | None,
      }
    """
    mastery = student.get("mastery_scores", {})
    style = student.get("learning_style", "visual-first")

    # Find the first concept not yet mastered (mastery < 80%)
    next_concept = None
    for concept in CONCEPT_ORDER:
        score = mastery.get(concept, 0)
        if score < 80:
            # Check prerequisites are met (≥60%)
            prereqs = CONCEPT_GRAPH[concept]["prerequisites"]
            prereqs_met = all(mastery.get(p, 0) >= 60 for p in prereqs)
            if prereqs_met:
                next_concept = concept
                break

    path = LEARNING_PATHS.get(style, LEARNING_PATHS["visual-first"])

    return {
        "next_concept": next_concept,
        "learning_style": style,
        "learning_path": path,
    }
