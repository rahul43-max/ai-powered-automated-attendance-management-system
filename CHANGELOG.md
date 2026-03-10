# Changelog

## 2026-02-24

### Added
- New professional project structure:
  - `backend/`
  - `frontend/`
  - `database/`
  - `models/`
- Backend app factory and API blueprint:
  - `backend/app/__init__.py`
  - `backend/app/api.py`
- Backend service modules:
  - `backend/app/db.py`
  - `backend/app/attendance.py`
  - `backend/app/recognition.py`
  - `backend/app/roster.py`
  - `backend/app/settings.py`
- Operational scripts:
  - `backend/scripts/capture_faces.py`
  - `backend/scripts/train_embeddings.py`
  - `backend/scripts/bootstrap_roster.py`
  - `backend/scripts/probe_recognition.py`
- New frontend dashboard:
  - `frontend/index.html`
  - `frontend/styles.css`
  - `frontend/app.js`
- Runtime entrypoint:
  - `backend/run.py`
- Project memory docs:
  - `STATUS.md`
  - `CHANGELOG.md`

### Improved
- Recognition pipeline stability:
  - multi-frame sampling per check
  - padded face ROI cropping
  - OpenCV Haar-based detector matching training flow
- Override handling:
  - clearer API error responses
  - frontend validation and safer submit behavior
- Documentation:
  - rewritten `README.md` for new architecture and run flow

### Notes
- `src/` remains in repo as legacy work.
- Active runtime path is `backend/` + `frontend/`.
