import os
import pickle
import time
from typing import Any

import numpy as np

from config import settings


def _safe_imports():
    try:
        import cv2  # type: ignore
        from deepface import DeepFace  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Missing runtime dependencies. Install opencv-python and deepface.") from exc
    return cv2, DeepFace


def _load_embedding_payload() -> dict:
    if not os.path.exists(settings.embeddings_path):
        raise FileNotFoundError(
            f"Embeddings file not found: {settings.embeddings_path}. Run train_model.py first."
        )
    with open(settings.embeddings_path, "rb") as f:
        return pickle.load(f)


def _detect_face_boxes_cv2(frame: Any) -> list[tuple[int, int, int, int]]:
    cv2, _ = _safe_imports()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # Smaller minimum size improves distant classroom CCTV pickup.
    faces = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]


def load_known_faces() -> tuple[list[np.ndarray], list[str], str]:
    data = _load_embedding_payload()
    encodings = [np.array(e, dtype=np.float64) for e in data.get("encodings", [])]
    names = [str(n) for n in data.get("names", [])]
    model_name = str(data.get("model_name", settings.model_name))
    if not encodings or not names:
        raise ValueError("Embeddings file is empty. Train with enrolled class data first.")
    return encodings, names, model_name


def load_student_profile_embeddings(student_id: str) -> tuple[list[np.ndarray], str]:
    data = _load_embedding_payload()
    model_name = str(data.get("model_name", settings.model_name))
    out: list[np.ndarray] = []

    profiles = data.get("profiles", {})
    if isinstance(profiles, dict):
        for label, profile in profiles.items():
            if not isinstance(profile, dict):
                continue
            sid = str(profile.get("student_id", ""))
            if sid == student_id or str(label).startswith(f"{student_id}_"):
                emb_rows = profile.get("embeddings", [])
                if isinstance(emb_rows, list):
                    for row in emb_rows:
                        out.append(np.array(row, dtype=np.float64))

    # Backward compatibility: fallback to centroid entries
    if not out:
        encodings = [np.array(e, dtype=np.float64) for e in data.get("encodings", [])]
        names = [str(n) for n in data.get("names", [])]
        for idx, label in enumerate(names):
            if label.startswith(f"{student_id}_"):
                out.append(encodings[idx])

    if not out:
        raise ValueError(
            f"No profile embeddings found for {student_id}. Capture images and retrain."
        )
    return out, model_name


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 1.0
    return float(1 - np.dot(a, b) / denom)


def distance_to_accuracy(distance: float) -> float:
    # Cosine distance is expected mostly in [0, 1] for this pipeline.
    d = max(0.0, min(1.0, float(distance)))
    return round((1.0 - d) * 100.0, 4)


def is_valid_match(distance: float) -> bool:
    accuracy = distance_to_accuracy(distance)
    return distance <= settings.match_threshold and accuracy >= settings.min_match_accuracy


def best_match(
    embedding: np.ndarray,
    known_encodings: list[np.ndarray],
    known_names: list[str],
) -> tuple[str, float, float]:
    best_name = "Unknown"
    best_distance = 999.0
    best_idx = -1

    for idx, known in enumerate(known_encodings):
        dist = cosine_distance(embedding, known)
        if dist < best_distance:
            best_distance = dist
            best_idx = idx

    best_accuracy = distance_to_accuracy(best_distance)
    if best_idx >= 0 and is_valid_match(best_distance):
        best_name = known_names[best_idx]
    return best_name, best_distance, best_accuracy


def detect_faces_in_frame(frame: Any) -> list[dict[str, Any]]:
    _, DeepFace = _safe_imports()
    faces = DeepFace.extract_faces(
        img_path=frame,
        detector_backend=settings.detector_backend,
        enforce_detection=False,
    )
    if isinstance(faces, dict) and "face" in faces:
        return [faces]
    if isinstance(faces, list):
        return faces
    return []


def extract_embedding(face_roi: Any, model_name: str) -> np.ndarray | None:
    _, DeepFace = _safe_imports()
    reps = DeepFace.represent(
        img_path=face_roi,
        model_name=model_name,
        detector_backend="skip",
        enforce_detection=False,
    )
    if not reps:
        return None
    return np.array(reps[0]["embedding"], dtype=np.float64)


def detect_known_students_once(sample_frames: int = 10) -> list[tuple[str, float]]:
    cv2, _ = _safe_imports()
    known_encodings, known_names, model_name = load_known_faces()

    cap = cv2.VideoCapture(settings.camera_index)
    if not cap.isOpened():
        raise RuntimeError("Could not access camera.")

    frame_samples: list[Any] = []
    for _ in range(sample_frames):
        ret, frame = cap.read()
        if ret:
            frame_samples.append(frame)
        time.sleep(0.03)
    cap.release()

    if not frame_samples:
        raise RuntimeError("Could not read frames from camera.")

    hit_count: dict[str, int] = {}
    best_dist: dict[str, float] = {}
    for frame in frame_samples:
        for x, y, w, h in _detect_face_boxes_cv2(frame):
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

            name, distance, _accuracy = best_match(emb, known_encodings, known_names)
            if name == "Unknown":
                continue

            hit_count[name] = hit_count.get(name, 0) + 1
            prev = best_dist.get(name, 999.0)
            if distance < prev:
                best_dist[name] = distance

    detections: list[tuple[str, float]] = []
    for name, count in hit_count.items():
        # Require at least two supporting frames for stability.
        if count >= 2:
            detections.append((name, best_dist[name]))
    return detections
