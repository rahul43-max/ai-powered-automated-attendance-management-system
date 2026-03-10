import os
import pickle
import sys

import cv2
import numpy as np


def _import_deepface():
    try:
        from deepface import DeepFace  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Missing dependency 'deepface'. Install it before training.") from exc
    return DeepFace


def _extract_face_roi_cv2(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    if len(faces) == 0:
        return None

    # Largest face is most likely the enrolled student.
    x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
    pad = 12
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img.shape[1], x + w + pad)
    y2 = min(img.shape[0], y + h + pad)
    roi = img[y1:y2, x1:x2]
    if roi.size == 0:
        return None
    return roi


def _represent_from_roi(DeepFace, face_roi, model_name: str):
    return DeepFace.represent(
        img_path=face_roi,
        model_name=model_name,
        detector_backend="skip",
        enforce_detection=False,
    )


def _parse_identity(folder_name: str) -> tuple[str, str]:
    if "_" not in folder_name:
        return folder_name, folder_name
    sid, full_name = folder_name.split("_", 1)
    return sid, full_name.replace("_", " ")


def _safe_reconfigure_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _collect_student_embeddings(DeepFace, student_path: str, model_name: str) -> list[list[float]]:
    out: list[list[float]] = []
    for image_file in sorted(os.listdir(student_path)):
        if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        image_path = os.path.join(student_path, image_file)
        try:
            face_roi = _extract_face_roi_cv2(image_path)
            if face_roi is None:
                continue
            embedding_objs = _represent_from_roi(
                DeepFace=DeepFace,
                face_roi=face_roi,
                model_name=model_name,
            )
            if embedding_objs:
                emb = embedding_objs[0]["embedding"]
                out.append([float(v) for v in emb])
        except Exception:
            continue
    return out


def train_model() -> None:
    """
    Build 360-degree profile embeddings for each student folder:
    data/known_faces/<ROLLNO>_<Name>/*.jpg

    Output format keeps both:
    - profiles: per-student multi-embedding lists (new strict runtime path)
    - encodings/names: centroid compatibility for older scripts
    """
    _safe_reconfigure_stdout()
    print("[*] Starting model training from enrolled student folders...")

    known_faces_dir = os.path.join("data", "known_faces")
    if not os.path.exists(known_faces_dir):
        print(f"[!] Directory not found: {known_faces_dir}")
        return

    student_folders = sorted(os.listdir(known_faces_dir))
    if not student_folders:
        print("[!] No student data found. Capture enrollment images first.")
        return

    DeepFace = _import_deepface()
    model_name = "Facenet"

    # Backward-compatible centroid output
    known_face_encodings: list[np.ndarray] = []
    known_face_names: list[str] = []

    # New profile output for targeted double verification
    profiles: dict[str, dict] = {}

    for folder_name in student_folders:
        student_path = os.path.join(known_faces_dir, folder_name)
        if not os.path.isdir(student_path):
            continue

        student_id, full_name = _parse_identity(folder_name)
        embeddings = _collect_student_embeddings(DeepFace, student_path, model_name)

        if not embeddings:
            print(f"    [!] {folder_name}: no valid face embeddings")
            continue

        emb_array = np.array(embeddings, dtype=np.float64)
        centroid = np.mean(emb_array, axis=0)
        known_face_encodings.append(centroid)
        known_face_names.append(folder_name)

        profiles[folder_name] = {
            "student_id": student_id,
            "full_name": full_name,
            "model_name": model_name,
            "embeddings": embeddings,
            "centroid": [float(v) for v in centroid],
            "samples_used": len(embeddings),
        }

        print(f"    [+] {folder_name}: profile built from {len(embeddings)} images")

    model_path = os.path.join("src", "face_encodings.pkl")
    payload = {
        "model_name": model_name,
        "encodings": known_face_encodings,
        "names": known_face_names,
        "profiles": profiles,
    }
    with open(model_path, "wb") as f:
        pickle.dump(payload, f)

    print(f"[SUCCESS] Model saved to {model_path}")
    print(f"[*] Students profiled: {len(profiles)}")


if __name__ == "__main__":
    train_model()
