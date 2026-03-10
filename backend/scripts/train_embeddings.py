import pickle
import sys
from pathlib import Path

import cv2
import numpy as np
from deepface import DeepFace

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.settings import settings


def _face_roi(path: Path):
    img = cv2.imread(str(path))
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(60, 60))
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
    pad = 12
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img.shape[1], x + w + pad)
    y2 = min(img.shape[0], y + h + pad)
    return img[y1:y2, x1:x2]


def train() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    root = Path(settings.known_faces_dir)
    if not root.exists():
        raise RuntimeError(f"known_faces folder missing: {root}")

    known_encodings = []
    known_names = []
    model_name = "Facenet"

    for folder in sorted(root.iterdir()):
        if not folder.is_dir():
            continue
        embs = []
        files = sorted([p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")])
        for f in files:
            roi = _face_roi(f)
            if roi is None:
                continue
            reps = DeepFace.represent(
                img_path=roi,
                model_name=model_name,
                detector_backend="skip",
                enforce_detection=False,
            )
            if reps:
                embs.append(reps[0]["embedding"])
        if embs:
            known_encodings.append(np.mean(embs, axis=0))
            known_names.append(folder.name)
            print(f"{folder.name}: encoded from {len(embs)} images")
        else:
            print(f"{folder.name}: no valid face embeddings")

    out = Path(settings.embeddings_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names, "model_name": model_name}, f)
    print(f"saved: {out} | identities={len(known_names)}")


if __name__ == "__main__":
    train()
