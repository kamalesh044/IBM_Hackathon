"""
ml/models/recommendation_model.py

Rule-based learning-style detection and resource recommendation.
Kept as a "model" class for architectural consistency — can be replaced
with a collaborative-filtering model later.
"""
from __future__ import annotations
from utils.constants import CONCEPT_ORDER, MASTERY_TARGET, MASTERY_PREREQ_MIN
from concept_graph import CONCEPT_GRAPH


LEARNING_PATHS = {
    "example-first":  "Short concept video -> Worked example -> 5 practice questions",
    "practice-first": "Quick concept summary -> Practice problems -> Adaptive difficulty drills",
    "visual-first":   "Visual diagram / animation -> Step-by-step walkthrough -> Guided problems",
}


class RecommendationModel:
    """
    Derives a student's learning style from attempt history and recommends
    the next concept + learning path.
    """

    def derive_style(self, attempt_history: list) -> str:
        """
        Infer learning style from activity_type performance.
        Returns: 'example-first' | 'practice-first' | 'visual-first'
        """
        if not attempt_history:
            return "visual-first"

        example_scores  = [a["score"] for a in attempt_history if a.get("activity_type") == "worked_example"]
        practice_scores = [a["score"] for a in attempt_history if a.get("activity_type") == "practice"]
        visual_scores   = [a["score"] for a in attempt_history if a.get("activity_type") == "visual"]

        avgs = {
            "example-first":  sum(example_scores)  / len(example_scores)  if example_scores  else 0,
            "practice-first": sum(practice_scores) / len(practice_scores) if practice_scores else 0,
            "visual-first":   sum(visual_scores)   / len(visual_scores)   if visual_scores   else 0,
        }

        best = max(avgs, key=avgs.get)
        # Only return non-visual if there's actual signal
        if avgs[best] > 0:
            return best
        return "visual-first"

    def next_concept(self, mastery: dict) -> str | None:
        """Return the first unmastered concept whose prereqs are satisfied."""
        for concept in CONCEPT_ORDER:
            score = mastery.get(concept, 0)
            if score < MASTERY_TARGET:
                prereqs = CONCEPT_GRAPH[concept]["prerequisites"]
                if all(mastery.get(p, 0) >= MASTERY_PREREQ_MIN for p in prereqs):
                    return concept
        return None

    def recommend(self, student: dict) -> dict:
        mastery = student.get("mastery_scores", {})
        style   = student.get("learning_style", "visual-first")
        nc      = self.next_concept(mastery)
        path    = LEARNING_PATHS.get(style, LEARNING_PATHS["visual-first"])
        return {
            "next_concept":   nc,
            "learning_style": style,
            "learning_path":  path,
        }


# Module-level singleton
_rec_model: RecommendationModel | None = None

def get_recommendation_model() -> RecommendationModel:
    global _rec_model
    if _rec_model is None:
        _rec_model = RecommendationModel()
    return _rec_model
