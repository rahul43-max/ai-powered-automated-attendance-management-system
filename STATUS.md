# Project Status (Quick Resume)

## Current State
- New clean architecture is active:
  - `backend/` (API + business logic)
  - `frontend/` (dashboard UI)
  - `database/attendance.db` (runtime DB)
  - `models/face_encodings.pkl` (trained embeddings)
- Old `src/` code exists but is legacy for this project phase.

## Last Known Working Flow
1. Install deps:
```powershell
python -m pip install -r requirements.txt
python -m pip install tf-keras
```
2. Capture images:
```powershell
python backend\scripts\capture_faces.py --name "Nithish Kumar" --id "23R91A05L6" --count 40
```
3. Train embeddings:
```powershell
python backend\scripts\train_embeddings.py
```
4. Sync roster:
```powershell
python backend\scripts\bootstrap_roster.py --class-id CSE-A-2026
```
5. Probe recognition:
```powershell
$env:ATT_MATCH_THRESHOLD="0.90"
python backend\scripts\probe_recognition.py
```
6. Run app:
```powershell
$env:ATT_MATCH_THRESHOLD="0.90"
python backend\run.py
```
7. Open dashboard:
```text
http://127.0.0.1:5000
```

## Known Issues
- Recognition is environment-sensitive (lighting, pose, camera quality).
- Some runs detect well, some return 0 detections; threshold tuning + better enrollment data needed.
- Override works when valid `period_id` + `student_id` row exists in `final_attendance`.

## Immediate Next Tasks
1. Add multi-student enrolled dataset (not just one student).
2. Add confidence diagnostics in UI (per-check distances).
3. Add auth/roles (admin/lecturer).
4. Add report export (CSV/PDF).
5. Add async background worker for long period runs.

## Resume Command
```powershell
cd "c:\Users\nithi\OneDrive\Desktop\IOMP"
$env:ATT_MATCH_THRESHOLD="0.90"
python backend\run.py
```
