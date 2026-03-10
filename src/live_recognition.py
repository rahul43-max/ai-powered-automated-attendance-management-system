from recognition_engine import detect_known_students_once


def run_live_recognition() -> None:
    print("[*] Single-shot known-student recognition (locked class only)")
    print("[*] Capturing one frame from camera and matching against enrolled students...")
    detections = detect_known_students_once()
    if not detections:
        print("[*] No enrolled students detected in this shot.")
        return
    print("[*] Detected students:")
    for label, distance in detections:
        print(f"    - {label} (distance={distance:.4f})")


if __name__ == "__main__":
    run_live_recognition()
