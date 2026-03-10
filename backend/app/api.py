from flask import Blueprint, jsonify, request

from . import db
from .attendance import run_period
from .recognition import probe_recognition
from .settings import settings


api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/health")
def health():
    return jsonify({"status": "ok"})


@api.get("/config")
def config():
    return jsonify(
        {
            "camera_index": settings.camera_index,
            "match_threshold": settings.match_threshold,
            "default_duration_minutes": settings.default_duration_minutes,
            "default_checks_count": settings.default_checks_count,
            "default_presence_threshold": settings.default_presence_threshold,
            "min_instances_required": settings.min_instances_required,
        }
    )


@api.get("/classes")
def classes():
    return jsonify(db.list_classes())


@api.get("/classes/<class_id>/students")
def class_students(class_id: str):
    return jsonify([dict(r) for r in db.get_class_students(class_id)])


@api.get("/periods")
def periods():
    limit = int(request.args.get("limit", "50"))
    return jsonify([dict(r) for r in db.list_periods(limit)])


@api.get("/periods/<int:period_id>")
def period(period_id: int):
    row = db.get_period(period_id)
    if row is None:
        return jsonify({"error": "period not found"}), 404
    return jsonify(dict(row))


@api.post("/periods/run")
def run():
    body = request.get_json(force=True)
    try:
        period_id = run_period(
            class_id=body["class_id"],
            duration_minutes=int(body.get("duration_minutes", settings.default_duration_minutes)),
            checks_count=int(body.get("checks_count", settings.default_checks_count)),
            threshold=float(body.get("threshold", settings.default_presence_threshold)),
            min_instances=int(body.get("min_instances", settings.min_instances_required)),
            seconds_per_minute=float(body.get("seconds_per_minute", 1.0)),
        )
        return jsonify({"period_id": period_id}), 201
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400


@api.get("/periods/<int:period_id>/attendance")
def attendance(period_id: int):
    return jsonify([dict(r) for r in db.get_final_attendance(period_id)])


@api.get("/periods/<int:period_id>/checks")
def checks(period_id: int):
    return jsonify([dict(r) for r in db.get_period_checks(period_id)])


@api.get("/periods/<int:period_id>/detections")
def detections(period_id: int):
    return jsonify([dict(r) for r in db.get_detection_logs(period_id)])


@api.get("/periods/<int:period_id>/overrides")
def overrides(period_id: int):
    return jsonify([dict(r) for r in db.get_overrides(period_id)])


@api.post("/periods/<int:period_id>/override")
def override(period_id: int):
    body = request.get_json(force=True)
    try:
        db.apply_override(
            period_id=period_id,
            student_id=body["student_id"],
            new_status=body["new_status"],
            lecturer=body.get("lecturer", "unknown_lecturer"),
            reason=body.get("reason", ""),
        )
        return jsonify({"status": "ok"})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400


@api.get("/recognition/probe")
def probe():
    try:
        return jsonify(probe_recognition())
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
