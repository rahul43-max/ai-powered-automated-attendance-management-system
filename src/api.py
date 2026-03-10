import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from database import (
    apply_override,
    get_class_students,
    get_detection_logs,
    get_final_attendance,
    get_verification_attempts,
    get_notifications,
    get_overrides,
    get_period,
    get_period_checks,
    list_classes,
    list_periods,
    auth_user,
    get_sms_logs,
)
from cctv_daemon import execute_60_minute_period

app = Flask(__name__)
# Enable CORS for React integration during dev
CORS(app)

# Serve static files from the new React build folder (frontend/dist)
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path and os.path.exists(os.path.join(WEB_DIR, path)):
        return send_from_directory(WEB_DIR, path)
    return send_from_directory(WEB_DIR, "index.html")


@app.post("/api/auth/login")
def login():
    body = request.get_json(force=True)
    user_id = body.get("user_id")
    password = body.get("password")
    
    user_row = auth_user(user_id, password)
    if not user_row:
        return jsonify({"error": "Invalid credentials"}), 401
        
    return jsonify({
        "user_id": user_row["user_id"],
        "role": user_row["role"],
        "full_name": user_row["full_name"],
        "token": "mock_jwt_token_tkrec_auth"
    })


@app.get("/api/sms_logs")
def get_sms():
    return jsonify([dict(r) for r in get_sms_logs()])


@app.post("/periods/run")
def run_period():
    body = request.get_json(force=True)
    try:
        period_id = execute_60_minute_period(
            class_id=body["class_id"],
            faculty_id=body.get("faculty_id", "FACULTY_01"),
            subject_code=body.get("subject_code", "AUTO"),
            subject_name=body.get("subject_name", "AUTO PERIOD"),
            location_type=body.get("location_type", "CLASSROOM"),
            location_name=body.get("location_name", "ROOM-NA"),
            camera_index=int(body.get("camera_index", 0)),
            slot_label=body.get("slot_label", "MANUAL-TRIGGER"),
            timetable_id=body.get("timetable_id"),
            test_mode=bool(body.get("test_mode", True)),
            seconds_per_minute=float(body.get("seconds_per_minute", 1.0)),
            faculty_phone=body.get("faculty_phone"),
            faculty_whatsapp=body.get("faculty_whatsapp"),
        )
        return jsonify({"period_id": period_id}), 201
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400


@app.get("/periods")
def periods():
    rows = list_periods(limit=int(request.args.get("limit", "50")))
    return jsonify([dict(r) for r in rows])


@app.get("/periods/<int:period_id>")
def period(period_id: int):
    row = get_period(period_id)
    if row is None:
        return jsonify({"error": "period not found"}), 404
    return jsonify(dict(row))


@app.get("/periods/<int:period_id>/attendance")
def get_attendance(period_id: int):
    rows = get_final_attendance(period_id)
    payload = [
        {
            "student_id": r["student_id"],
            "full_name": r["full_name"],
            "detections_count": r["detections_count"],
            "checks_count": r["checks_count"],
            "detection_ratio": r["detection_ratio"],
            "ai_status": r["ai_status"],
            "final_status": r["final_status"],
        }
        for r in rows
    ]
    return jsonify(payload)


@app.get("/periods/<int:period_id>/checks")
def period_checks(period_id: int):
    return jsonify([dict(r) for r in get_period_checks(period_id)])


@app.get("/periods/<int:period_id>/detections")
def detections(period_id: int):
    return jsonify([dict(r) for r in get_detection_logs(period_id)])


@app.get("/periods/<int:period_id>/attempts")
def attempts(period_id: int):
    return jsonify([dict(r) for r in get_verification_attempts(period_id)])


@app.get("/periods/<int:period_id>/overrides")
def overrides(period_id: int):
    return jsonify([dict(r) for r in get_overrides(period_id)])


@app.get("/notifications")
def notifications():
    period_id = request.args.get("period_id")
    if period_id is None:
        rows = get_notifications()
    else:
        rows = get_notifications(int(period_id))
    return jsonify([dict(r) for r in rows])


@app.post("/periods/<int:period_id>/override")
def override(period_id: int):
    body = request.get_json(force=True)
    try:
        apply_override(
            period_id=period_id,
            student_id=body["student_id"],
            new_status=body["new_status"],
            lecturer=body.get("lecturer", "unknown_lecturer"),
            reason=body.get("reason", ""),
        )
        return jsonify({"status": "ok"})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400


@app.get("/classes")
def classes():
    return jsonify(list_classes())


@app.get("/classes/<class_id>/students")
def students(class_id: str):
    rows = get_class_students(class_id)
    return jsonify([dict(r) for r in rows])


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
