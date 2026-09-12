# AI Learning Intelligence Platform

> Predictive Concept-Readiness · Root-Cause Analysis · Personalized Learning · Mentor Intervention

---

## Quick Start

### 1. Start the Backend (FastAPI)
```powershell
.\start_backend.ps1
# or manually:
cd backend
python -m uvicorn main:app --reload --port 8000
```
Backend runs at: http://localhost:8000  
API docs: http://localhost:8000/docs

### 2. Start the Frontend (React)
In a second terminal:
```powershell
.\start_frontend.ps1
# or manually:
cd frontend
npm run dev
```
Frontend runs at: http://localhost:3000

---

## Project Structure

```
IBM_hackathon/
├── backend/
│   ├── main.py                  # FastAPI app — all endpoints
│   ├── concept_graph.py         # Knowledge graph (4 DS concepts)
│   ├── root_cause.py            # Root-cause tracer + explanation
│   ├── recommendation.py        # Learning-method recommendations
│   ├── seed_data.py             # 7 students + 2 mentors + sample data
│   ├── train_model.py           # Offline ML training script
│   ├── model/
│   │   ├── readiness_model.joblib
│   │   └── feature_names.json
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Router
│   │   ├── api.js               # Axios API client
│   │   ├── utils.js             # Risk colors, formatting
│   │   ├── components/
│   │   │   ├── Layout.jsx       # Nav header + footer disclaimer
│   │   │   ├── MasteryBars.jsx  # Concept mastery progress bars
│   │   │   ├── RiskBadge.jsx    # Traffic-light risk indicator
│   │   │   ├── QuizSubmitForm.jsx    # Live quiz + predict trigger
│   │   │   └── FollowUpQuizForm.jsx  # Post-intervention quiz
│   │   └── pages/
│   │       ├── Home.jsx             # Landing/nav hub
│   │       ├── FacultyDashboard.jsx # Class overview, risk table
│   │       ├── StudentList.jsx      # All students grid
│   │       ├── StudentProfile.jsx   # Full drill-down + charts
│   │       ├── MentorDashboard.jsx  # Notifications + sessions
│   │       └── StudentDashboard.jsx # Student self-view + quiz
│   └── package.json
│
├── start_backend.ps1
├── start_frontend.ps1
└── README.md
```

---

## Demo Script (Judge Walk-Through)

1. **Open Faculty Dashboard** (`/faculty`)
   - See risk counts: 🟢 Low / 🟡 Medium / 🔴 High
   - View class average mastery bars for all 4 concepts
   - See intervention summary: X sessions, avg +Y% improvement
   - Click a high-risk student → drill-down profile

2. **Student Profile** (`/faculty/student/s005`)
   - Mastery bars (concept by concept)
   - AI prediction: "Risk HIGH (82%) — Contributing factors: …"
   - Root-cause: "Difficulty with Tree Traversal traces back to Arrays/Linked Lists"
   - Recommendation: "What to learn: Recursion | How: Visual diagram -> Step-by-step -> Guided problems"
   - Intervention history chart (before/after bars)

3. **Trigger a live notification**
   - Go to Student View (`/student`), select any student
   - Submit a quiz with low score + high errors → get 🔴 prediction
   - "🔔 Mentor notification auto-created!" appears in the result

4. **Mentor Dashboard** (`/mentor`)
   - Bell shows unread count (2 pre-seeded + any live one)
   - Pending notification card: student, concept, risk %, root cause, proposed slot
   - Click **Confirm** → moves to Upcoming Sessions

5. **Mark Session Complete**
   - Click ✓ Mark Complete on an upcoming session
   - Follow-up quiz form appears
   - Enter post-intervention score → see "Recursion: 42% → 71% (+29%)"

6. **Return to Faculty Dashboard**
   - Intervention summary updates with new session
   - Student's mastery bars reflect post-session improvement

---

## Key APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/students` | All students with risk predictions |
| GET | `/students/{id}` | Full profile + prediction + recommendation |
| POST | `/students/{id}/quiz` | Submit quiz, update mastery, auto-schedule |
| POST | `/predict` | Raw ML prediction for student + concept |
| GET | `/notifications?mentor_id=X` | Mentor notification inbox |
| PATCH | `/notifications/{id}` | Confirm / reschedule / decline |
| GET | `/sessions` | Confirmed sessions |
| POST | `/sessions/{id}/complete` | Mark session done |
| POST | `/interventions/followup` | Log post-session quiz + delta |
| GET | `/interventions/summary` | Aggregate improvement stats |
| GET | `/dashboard/overview` | Faculty class overview |

---

## ML Model

- **Algorithm:** RandomForestClassifier (scikit-learn)
- **Training data:** 400 synthetic rows, rule-derived labels
- **Features:** `prereq_score_pct`, `num_attempts`, `repeated_error_count`, `time_per_q_ratio`, `days_since_last_practice`, `sub_concepts_attempted_pct`, `engagement_score`, `consistency_score`
- **Performance:** 99% accuracy on held-out test set
- **Risk labels:** 🟢 <30% | 🟡 30–60% | 🔴 >60%
- **Explainability:** Template-based, top-3 contributing features per prediction

> ⚠️ **Predictions are directional, not diagnostic.**
