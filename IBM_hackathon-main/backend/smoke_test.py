"""
Smoke test for the new structured backend (v2).
Run from: backend/   ->  python smoke_test.py
"""
import sys, os
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.insert(0, '.')

from database import db
from services.risk_service import predict_risk, current_concept
from services.recommendation_service import recommend_next
from services.intervention_service import intervention_summary
from routers.faculty import class_overview

# Test 1: Predictions
print('=== Predictions ===')
for s in db['students'].values():
    cc   = current_concept(s)
    pred = predict_risk(s, cc)
    name = s['name']
    print(f'  {name[:20]:20s} | {cc[:25]:25s} | {pred["risk_label"]:6s} {round(pred["risk_probability"]*100)}%')

# Test 2: Dashboard overview
print()
print('=== Dashboard Overview ===')
ov = class_overview()
rc = ov['risk_counts']
print(f'  Low={rc["low"]}  Medium={rc["medium"]}  High={rc["high"]}')
print(f'  At-risk students: {len(ov["at_risk_students"])}')
print(f'  Intervention summary: {ov["intervention_summary"]}')

# Test 3: Notifications
print()
print('=== Seeded Notifications ===')
for n in db['notifications'].values():
    name = n.get('student_name', n['student_id'])
    print(f'  [{n["status"]}] {name} - {n["concept"]} - Risk {n["risk_score"]}%')

# Test 4: Services
print()
print('=== Service Layer ===')
from services.mastery_service import bkt_mastery_scores
s0 = list(db['students'].values())[0]
bkt = bkt_mastery_scores(s0)
print(f'  BKT mastery for {s0["name"]}: {bkt}')

rec = recommend_next(s0)
print(f'  Recommendation: next={rec["next_concept"]}, style={rec["learning_style"]}')

# Test 5: ML model
print()
print('=== ML Model ===')
from ml.models.risk_model import get_risk_model
model = get_risk_model()
print(f'  Loaded: {model.loaded}')
feat = model.feature_vector(s0, 'Binary Search Trees', {})
print(f'  Feature vector keys: {list(feat.keys())}')

print()
print('All smoke tests passed.')
