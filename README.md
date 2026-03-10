# AI Attendance System (Professional Structure)

## Quick Resume
- Current working state: `STATUS.md`
- Work history: `CHANGELOG.md`

## Project Layout
- `frontend/`: production-style dashboard UI.
- `backend/`: Flask API, services, business logic.
- `database/`: SQLite DB file (`attendance.db`).
- `models/`: trained face embeddings (`face_encodings.pkl`).
- `data/known_faces/`: enrolled student image folders.

## Core Features Implemented
- Period-wise randomized attendance checks.
- Multi-instance verification per period.
- Threshold-based present/absent decision.
- Fixed enrolled-class roster only.
- Lecturer override with audit logs.
- API + professional dashboard frontend.

## Setup
```powershell
cd "c:\Users\nithi\OneDrive\Desktop\IOMP"
python -m pip install -r requirements.txt
python -m pip install tf-keras
```

## Enrollment and Training
Capture images (repeat for each student):
```powershell
python backend\scripts\capture_faces.py --name "Nithish Kumar" --id "23R91A05L6" --count 30
```

Train embeddings:
```powershell
python backend\scripts\train_embeddings.py
```

Quick recognition probe:
```powershell
python backend\scripts\probe_recognition.py
```

Sync class roster:
```powershell
python backend\scripts\bootstrap_roster.py --class-id CSE-A-2026
```

## Run Application
```powershell
$env:ATT_MATCH_THRESHOLD="0.85"
python backend\run.py
```

Open:
```text
http://127.0.0.1:5000
```

Override from terminal (optional):
```powershell
python -c "import sys; sys.path.append('backend'); from app import db; db.apply_override(1,'23R91A05L6','PRESENT','P.Swetha','Manual review')"
```

## API
- `GET /api/health`
- `GET /api/config`
- `GET /api/classes`
- `GET /api/classes/{class_id}/students`
- `GET /api/periods`
- `POST /api/periods/run`
- `GET /api/periods/{period_id}/attendance`
- `POST /api/periods/{period_id}/override`
- `GET /api/recognition/probe`

## Accuracy Tuning
- Increase `ATT_MATCH_THRESHOLD` (e.g., `0.88`) if recognition is too strict.
- Retake enrollment images with strong frontal lighting.
- Keep face centered during checks.
