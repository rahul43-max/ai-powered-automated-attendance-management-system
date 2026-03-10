import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    camera_index: int = int(os.getenv("ATT_CAMERA_INDEX", "0"))
    match_threshold: float = float(os.getenv("ATT_MATCH_THRESHOLD", "0.85"))

    default_duration_minutes: int = int(os.getenv("ATT_PERIOD_DURATION_MIN", "45"))
    default_checks_count: int = int(os.getenv("ATT_RANDOM_CHECKS_COUNT", "4"))
    default_presence_threshold: float = float(os.getenv("ATT_PRESENCE_THRESHOLD", "0.75"))
    min_instances_required: int = int(os.getenv("ATT_MIN_INSTANCES", "2"))

    db_path: str = str(ROOT_DIR / "database" / "attendance.db")
    embeddings_path: str = str(ROOT_DIR / "models" / "face_encodings.pkl")
    known_faces_dir: str = str(ROOT_DIR / "data" / "known_faces")


settings = Settings()
