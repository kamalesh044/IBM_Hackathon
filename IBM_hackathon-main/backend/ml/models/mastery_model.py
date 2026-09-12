"""
ml/models/mastery_model.py

Bayesian Knowledge Tracing (BKT) — lightweight implementation.

BKT models each concept as a Hidden Markov Model with 4 parameters:
    p_init   — P(mastered at start)
    p_learn  — P(transition: unmastered → mastered after attempt)
    p_forget — P(transition: mastered → unmastered)  [usually ~0]
    p_guess  — P(correct | unmastered)
    p_slip   — P(incorrect | mastered)

After each response the posterior P(mastered) is updated via Bayes' rule.
The final mastery score (0–100) is this posterior × 100.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class BKTParams:
    p_init:   float = 0.10
    p_learn:  float = 0.20
    p_forget: float = 0.005
    p_guess:  float = 0.25
    p_slip:   float = 0.10


class BKTMasteryModel:
    """
    Per-student, per-concept mastery tracker using BKT.

    Usage:
        model = BKTMasteryModel()
        for response in [1, 0, 1, 1, 0, 1]:   # 1=correct, 0=incorrect
            model.update(response)
        print(model.mastery_score)   # 0–100
    """

    DEFAULT_PARAMS = {
        "Arrays/Linked Lists": BKTParams(p_init=0.15, p_learn=0.25),
        "Recursion":           BKTParams(p_init=0.10, p_learn=0.18),
        "Tree Traversal":      BKTParams(p_init=0.10, p_learn=0.20),
        "Binary Search Trees": BKTParams(p_init=0.08, p_learn=0.15),
    }

    def __init__(self, concept: str = "Recursion"):
        params = self.DEFAULT_PARAMS.get(concept, BKTParams())
        self.p      = params
        self._pL    = params.p_init   # P(mastered) — updated each step
        self.history: List[float] = []

    @property
    def p_mastered(self) -> float:
        return self._pL

    @property
    def mastery_score(self) -> float:
        """0–100 mastery score."""
        return round(self._pL * 100, 1)

    def update(self, correct: int) -> float:
        """
        Update mastery given one response.
        correct: 1 = correct, 0 = incorrect
        Returns updated p_mastered.
        """
        pL = self._pL
        p  = self.p

        if correct:
            # P(mastered | correct)
            num = pL * (1 - p.p_slip)
            den = num + (1 - pL) * p.p_guess
        else:
            # P(mastered | incorrect)
            num = pL * p.p_slip
            den = num + (1 - pL) * (1 - p.p_guess)

        pL_given_obs = num / den if den > 0 else pL

        # Transition
        pL_next = pL_given_obs * (1 - p.p_forget) + (1 - pL_given_obs) * p.p_learn
        self._pL = min(max(pL_next, 0.0), 1.0)
        self.history.append(self._pL)
        return self._pL

    def fit_history(self, responses: List[int]) -> float:
        """Run a full response sequence and return final mastery score."""
        for r in responses:
            self.update(r)
        return self.mastery_score

    @classmethod
    def score_from_attempts(cls, concept: str, attempt_history: list) -> float:
        """
        Convenience: compute BKT mastery from attempt_history dicts.
        Falls back to the stored score if no binary response data available.
        """
        relevant = [a for a in attempt_history if a.get("concept") == concept]
        if not relevant:
            return 0.0
        model = cls(concept)
        for a in relevant:
            score = a.get("score", 50)
            # Map score → binary: ≥60 = correct
            correct = 1 if score >= 60 else 0
            model.update(correct)
        return model.mastery_score
