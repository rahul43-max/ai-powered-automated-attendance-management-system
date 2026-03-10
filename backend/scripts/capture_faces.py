import argparse
import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.settings import settings


def capture(name: str, student_id: str, count: int) -> None:
    safe = f"{student_id}_{name.replace(' ', '_')}"
    out_dir = Path(settings.known_faces_dir) / safe
    out_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(settings.camera_index)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera.")

    print(f"Capturing {count} images for {safe}. Press C to capture, Q to quit.")
    i = 0
    while i < count:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, f"{i}/{count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Capture Faces", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("c"), ord("C")):
            path = out_dir / f"{safe}_{i}.jpg"
            cv2.imwrite(str(path), frame)
            print(f"saved: {path}")
            i += 1
        elif key in (ord("q"), ord("Q")):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"done: {i} images")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--count", type=int, default=30)
    args = parser.parse_args()
    capture(args.name, args.id, args.count)
