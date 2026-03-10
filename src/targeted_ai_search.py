import time
from datetime import datetime, timezone
from typing import Any, Optional

from config import settings
from database import get_conn, insert_detections, log_verification_attempt
from recognition_engine import (
    _detect_face_boxes_cv2,
    _safe_imports,
    cosine_distance,
    distance_to_accuracy,
    extract_embedding,
    is_valid_match,
    load_student_profile_embeddings,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _capture_classroom_frames(camera_index: int, scan_seconds: float, frame_interval: float) -> list[Any]:
    cv2, _ = _safe_imports()
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not access camera index {camera_index}.")

    frames: list[Any] = []
    start = time.time()
    while (time.time() - start) < scan_seconds:
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        time.sleep(max(0.01, frame_interval))
    cap.release()
    return frames


def targeted_student_search(student_id: str, camera_index: int) -> dict:
    """
    Strict targeted search for exactly one student profile in a classroom frame sequence.
    Match is valid only if:
    1) cosine distance <= ATT_MATCH_THRESHOLD
    2) accuracy score >= ATT_MIN_MATCH_ACCURACY (default 95)
    """
    result = {
        "found": False,
        "best_distance": None,
        "best_accuracy": None,
        "timestamp": _utc_now(),
        "model_name": settings.model_name,
        "detector_backend": "opencv_haar",
        "frames_scanned": 0,
        "faces_scanned": 0,
        "notes": "",
    }

    try:
        target_embeddings, model_name = load_student_profile_embeddings(student_id)
        result["model_name"] = model_name
    except Exception as exc:
        result["notes"] = f"profile_load_failed: {exc}"
        return result

    try:
        frames = _capture_classroom_frames(
            camera_index=camera_index,
            scan_seconds=settings.scan_seconds,
            frame_interval=settings.frame_sample_interval,
        )
    except Exception as exc:
        result["notes"] = f"camera_error: {exc}"
        return result

    result["frames_scanned"] = len(frames)
    if not frames:
        result["notes"] = "no_frames_captured"
        return result

    best_distance: Optional[float] = None
    face_counter = 0
    frame_fallback_counter = 0

    for frame in frames:
        face_boxes = _detect_face_boxes_cv2(frame)
        if not face_boxes:
            # Fallback path for difficult CCTV angles: try the full frame as one ROI.
            emb = extract_embedding(frame, model_name)
            if emb is not None:
                frame_fallback_counter += 1
                for known_emb in target_embeddings:
                    dist = cosine_distance(emb, known_emb)
                    if best_distance is None or dist < best_distance:
                        best_distance = dist
            continue

        for x, y, w, h in face_boxes:
            pad = 12
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(frame.shape[1], x + w + pad)
            y2 = min(frame.shape[0], y + h + pad)
            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                continue

            emb = extract_embedding(roi, model_name)
            if emb is None:
                continue

            face_counter += 1
            for known_emb in target_embeddings:
                dist = cosine_distance(emb, known_emb)
                if best_distance is None or dist < best_distance:
                    best_distance = dist

    result["faces_scanned"] = face_counter
    if frame_fallback_counter > 0:
        result["notes"] = f"frame_fallback_used:{frame_fallback_counter}"
    if best_distance is None:
        if face_counter == 0 and frame_fallback_counter == 0:
            result["notes"] = "no_faces_detected_in_scan_window"
        else:
            result["notes"] = "no_target_face_embedding_matchable"
        return result

    best_accuracy = distance_to_accuracy(best_distance)
    result["best_distance"] = float(best_distance)
    result["best_accuracy"] = float(best_accuracy)
    result["timestamp"] = _utc_now()

    if is_valid_match(best_distance):
        result["found"] = True
        result["notes"] = "match_confirmed"
    else:
        result["notes"] = "below_strict_threshold"
    return result


def execute_random_class_sweep(
    period_id: int,
    check_id: int,
    scheduled_student_id: str,
    scheduled_minute: int,
    camera_index: int,
) -> dict:
    """
    Run one targeted verification attempt for one student and persist complete audit logs.
    """
    with get_conn() as conn:
        student = conn.execute(
            "SELECT full_name FROM students WHERE student_id=?",
            (scheduled_student_id,),
        ).fetchone()

    if not student:
        result = {
            "found": False,
            "best_distance": None,
            "best_accuracy": None,
            "timestamp": _utc_now(),
            "model_name": settings.model_name,
            "detector_backend": "opencv_haar",
            "frames_scanned": 0,
            "faces_scanned": 0,
            "notes": "student_not_found_in_db",
        }
    else:
        result = targeted_student_search(
            student_id=scheduled_student_id,
            camera_index=camera_index,
        )

    if result["found"] and result["best_distance"] is not None and result["best_accuracy"] is not None:
        insert_detections(
            period_id=period_id,
            check_id=check_id,
            detections=[(scheduled_student_id, result["best_distance"], result["best_accuracy"])],
        )

    log_verification_attempt(
        period_id=period_id,
        check_id=check_id,
        student_id=scheduled_student_id,
        scheduled_minute=scheduled_minute,
        found=bool(result["found"]),
        best_distance=result["best_distance"],
        best_accuracy=result["best_accuracy"],
        min_required_accuracy=settings.min_match_accuracy,
        detector_backend=str(result.get("detector_backend", "opencv_haar")),
        model_name=str(result.get("model_name", settings.model_name)),
        camera_index=camera_index,
        notes=str(result.get("notes", "")),
        actual_ts=str(result.get("timestamp", _utc_now())),
    )
    return result
