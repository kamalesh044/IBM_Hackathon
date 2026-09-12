"""
Concept Root-Cause Tracer.
Walks backward through the prerequisite graph to find the deepest
prerequisite concept where mastery falls below the threshold.
"""

from concept_graph import CONCEPT_GRAPH


def trace_root_cause(
    concept: str,
    mastery_scores: dict,
    graph: dict = None,
    threshold: float = 50.0,
    _depth: int = 0,
    _max_depth: int = 10,
) -> str:
    """
    Returns the root-cause concept (deepest prerequisite below threshold).
    Falls back to the starting concept if no gap is found upstream.
    """
    if graph is None:
        graph = CONCEPT_GRAPH

    if _depth >= _max_depth:
        return concept

    prereqs = graph.get(concept, {}).get("prerequisites", [])
    if not prereqs:
        return concept

    for p in prereqs:
        if mastery_scores.get(p, 100.0) < threshold:
            return trace_root_cause(
                p,
                mastery_scores,
                graph,
                threshold,
                _depth + 1,
                _max_depth,
            )

    return concept


def build_root_cause_explanation(
    struggling_concept: str,
    root_cause_concept: str,
    mastery_scores: dict,
) -> str:
    """
    Produces a human-readable root-cause explanation string.
    """
    if root_cause_concept == struggling_concept:
        mastery = mastery_scores.get(struggling_concept, 0)
        return (
            f"Your difficulty with {struggling_concept} appears to be "
            f"a direct gap in this concept itself (mastery: {mastery:.0f}%). "
            "Focus on foundational practice here."
        )
    root_mastery = mastery_scores.get(root_cause_concept, 0)
    return (
        f"Your difficulty with {struggling_concept} traces back to a gap in "
        f"{root_cause_concept} (mastery: {root_mastery:.0f}%), not the topic itself. "
        f"Strengthening {root_cause_concept} first will unblock progress."
    )
