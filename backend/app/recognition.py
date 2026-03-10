import os
import pickle
import time
from typing import Any

import numpy as np

from .settings import settings


def _imports():
    import cv2  # type: ignore
    from deepface import DeepFace  # type: ignore

    return cv2, DeepFace


def load_embeddings() -> tuple[list[np.ndarray], list[str], str]:
    if not os.path.exists(settings.embeddings_path):
        raise FileNotFoundError(f"Embeddings not found: {settings.embeddings_path}")
    with open(settings.embeddings_path, "rb") as f:
        data = pickle.load(f)
    encodings = [np.array(v) for v in data.get("encodings", [])]
    names = data.get("names", [])
    model_name = data.get("model_name", "Facenet")
    if not encodings:
        raise ValueError("Embeddings are empty. Run training first.")
    return encodings, names, model_name


def _detect_boxes(frame: Any) -> list[tuple[int, int, int, int]]:
    cv2, _ = _imports()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(60, 60))
    return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]


def _embedding(face_roi: Any, model_name: str) -> np.ndarray | None:
    _, DeepFace = _imports()
    reps = DeepFace.represent(
        img_path=face_roi,
        model_name=model_name,
        detector_backend="skip",
        enforce_detection=False,
    )
    if not reps:
        return None
    return np.array(reps[0]["embedding"])


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 1.0
    return float(1 - np.dot(a, b) / denom)


def _best_match(emb: np.ndarray, known_embs: list[np.ndarray], known_names: list[str]) -> tuple[str, float]:
    best_name = "Unknown"
    best_dist = 999.0
    for i, k in enumerate(known_embs):
        d = _cosine(emb, k)
        if d < best_dist:
            best_dist = d
            best_name = known_names[i]
    if best_dist <= settings.match_threshold:
        return best_name, best_dist
    return "Unknown", best_dist


def detect_known_students_once(sample_frames: int = 10) -> list[tuple[str, float]]:
    cv2, _ = _imports()
    known_embs, known_names, model_name = load_embeddings()
    cap = cv2.VideoCapture(settings.camera_index)
    if not cap.isOpened():
        raise RuntimeError("Could not access camera.")

    frames = []
    for _ in range(sample_frames):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        time.sleep(0.03)
    cap.release()
    if not frames:
        raise RuntimeError("Could not read frames from camera.")

    hit_count: dict[str, int] = {}
    best_dist: dict[str, float] = {}
    for frame in frames:
        for x, y, w, h in _detect_boxes(frame):
            pad = 12
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(frame.shape[1], x + w + pad)
            y2 = min(frame.shape[0], y + h + pad)
            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                continue
            emb = _embedding(roi, model_name)
            if emb is None:
                continue
            name, dist = _best_match(emb, known_embs, known_names)
            if name == "Unknown":
                continue
            hit_count[name] = hit_count.get(name, 0) + 1
            best_dist[name] = min(dist, best_dist.get(name, 999.0))

    out: list[tuple[str, float]] = []
    for name, cnt in hit_count.items():
        if cnt >= 2:
            out.append((name, best_dist[name]))
    return out


def probe_recognition() -> dict:
    rows = detect_known_students_once(sample_frames=12)
    return {
        "threshold": settings.match_threshold,
        "detections": [{"label": label, "distance": dist} for label, dist in rows],
    }
