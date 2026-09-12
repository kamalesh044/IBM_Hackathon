"""services/root_cause_service.py — Root-cause tracing and explanation building."""
from __future__ import annotations
from concept_graph import CONCEPT_GRAPH
from utils.constants import CLASS_MEDIAN_TIME


ROOT_CAUSE_THRESHOLD = 50.0


def trace_root_cause(
    concept: str,
    mastery_scores: dict,
    threshold: float = ROOT_CAUSE_THRESHOLD,
    _depth: int = 0,
    _max_depth: int = 10,
) -> str:
    """Walk prereqs backward; return deepest concept below threshold."""
    if _depth >= _max_depth:
        return concept
    prereqs = CONCEPT_GRAPH.get(concept, {}).get("prerequisites", [])
    if not prereqs:
        return concept
    for p in prereqs:
        if mastery_scores.get(p, 100.0) < threshold:
            return trace_root_cause(p, mastery_scores, threshold, _depth + 1, _max_depth)
    return concept


def build_root_cause_text(struggling: str, root: str, mastery: dict) -> str:
    if root == struggling:
        m = mastery.get(struggling, 0)
        return (
            f"Your difficulty with {struggling} appears to be a direct gap in this concept "
            f"itself (mastery: {m:.0f}%). Focus on foundational practice here."
        )
    m = mastery.get(root, 0)
    return (
        f"Your difficulty with {struggling} traces back to a gap in {root} "
        f"(mastery: {m:.0f}%), not the topic itself. "
        f"Strengthening {root} first will unblock progress."
    )


def build_explanation(
    risk_prob: float,
    features: dict,
    top_features: list,
    root_cause: str,
    struggling: str,
    mastery: dict,
) -> str:
    from utils.helpers import risk_label
    label = risk_label(risk_prob)
    pct   = round(risk_prob * 100)
    parts = []
    for feat, importance in top_features[:3]:
        val = features.get(feat)
        if feat == "prereq_score_pct":
            parts.append(f"prerequisite mastery {val:.0f}%")
        elif feat == "repeated_error_count":
            parts.append(f"{int(val)} repeated error(s)")
        elif feat == "time_per_q_ratio":
            diff = (val - 1) * 100
            parts.append(f"time-per-question {abs(diff):.0f}% {'above' if diff > 0 else 'below'} class median")
        elif feat == "days_since_last_practice":
            parts.append(f"{int(val)} day(s) since last practice")
        elif feat == "num_attempts":
            parts.append(f"{int(val)} attempt(s) on prerequisite")
        elif feat == "sub_concepts_attempted_pct":
            parts.append(f"{val:.0f}% of sub-concepts attempted")
        elif feat == "engagement_score":
            parts.append(f"engagement score {val:.0f}%")
        elif feat == "consistency_score":
            parts.append(f"consistency score {val:.0f}%")

    factor_str = "; ".join(parts) if parts else "multiple factors"
    base = f"Risk: {label} ({pct}%). Contributing factors: {factor_str}."
    root_text = build_root_cause_text(struggling, root_cause, mastery)
    return f"{base} {root_text}"
