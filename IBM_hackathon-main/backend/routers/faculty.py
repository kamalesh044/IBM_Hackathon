from fastapi import APIRouter
from database import db
from services.risk_service import predict_risk, current_concept
from services.recommendation_service import recommend_next
from utils.helpers import risk_label

router = APIRouter(prefix="/dashboard", tags=["faculty"])


@router.get("/overview")
def class_overview():
    low = medium = high = 0
    at_risk_list  = []
    total_mastery: dict = {}

    for s in db["students"].values():
        cc   = current_concept(s)
        pred = predict_risk(s, cc)
        lbl  = pred["risk_label"]

        if lbl == "LOW":
            low += 1
        elif lbl == "MEDIUM":
            medium += 1
        else:
            high += 1
            at_risk_list.append({
                "student_id":       s["id"],
                "student_name":     s["name"],
                "concept":          cc,
                "risk_probability": pred["risk_probability"],
                "risk_label":       lbl,
                "root_cause_concept": pred["root_cause_concept"],
                "explanation":      pred["explanation"],
            })

        for concept, score in s["mastery_scores"].items():
            total_mastery.setdefault(concept, []).append(score)

    class_avg = {c: round(sum(v)/len(v), 1) for c, v in total_mastery.items()}

    from services.intervention_service import intervention_summary
    isummary = intervention_summary()

    return {
        "risk_counts":        {"low": low, "medium": medium, "high": high},
        "at_risk_students":   at_risk_list,
        "class_avg_mastery":  class_avg,
        "intervention_summary": {
            "total_sessions":  isummary["total_sessions"],
            "avg_improvement": isummary["avg_improvement"],
        },
    }
