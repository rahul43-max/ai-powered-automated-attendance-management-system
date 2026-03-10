import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Recognition
    model_name: str = os.getenv("ATT_MODEL_NAME", "Facenet")
    detector_backend: str = os.getenv("ATT_DETECTOR_BACKEND", "opencv")
    match_threshold: float = float(os.getenv("ATT_MATCH_THRESHOLD", "0.40"))
    min_match_accuracy: float = float(os.getenv("ATT_MIN_MATCH_ACCURACY", "95.0"))
    camera_index: int = int(os.getenv("ATT_CAMERA_INDEX", "0"))
    scan_seconds: float = float(os.getenv("ATT_SCAN_SECONDS", "3.0"))
    frame_sample_interval: float = float(os.getenv("ATT_FRAME_SAMPLE_INTERVAL", "0.1"))

    # Attendance policy
    strict_period_minutes: int = int(os.getenv("ATT_PERIOD_DURATION_MIN", "60"))
    grace_start_minutes: int = int(os.getenv("ATT_GRACE_START_MIN", "10"))
    active_window_minutes: int = int(os.getenv("ATT_ACTIVE_WINDOW_MIN", "40"))
    grace_end_minutes: int = int(os.getenv("ATT_GRACE_END_MIN", "10"))
    checks_per_student: int = int(os.getenv("ATT_CHECKS_PER_STUDENT", "2"))
    first_check_minute_start: int = int(os.getenv("ATT_FIRST_CHECK_START", "11"))
    first_check_minute_end: int = int(os.getenv("ATT_FIRST_CHECK_END", "30"))
    second_check_minute_start: int = int(os.getenv("ATT_SECOND_CHECK_START", "31"))
    second_check_minute_end: int = int(os.getenv("ATT_SECOND_CHECK_END", "40"))
    post_attendance_minute: int = int(os.getenv("ATT_POST_ATTENDANCE_MINUTE", "55"))
    presence_threshold: float = float(os.getenv("ATT_PRESENCE_THRESHOLD", "0.50"))
    min_instances_required: int = int(os.getenv("ATT_MIN_INSTANCES", "1"))
    seconds_per_minute: float = float(os.getenv("ATT_SECONDS_PER_MINUTE", "60.0"))
    daemon_poll_seconds: int = int(os.getenv("ATT_DAEMON_POLL_SECONDS", "30"))

    # Storage
    db_path: str = os.getenv("ATT_DB_PATH", "data/attendance.db")
    embeddings_path: str = os.getenv("ATT_EMBEDDINGS_PATH", "src/face_encodings.pkl")

    # Notification settings
    notify_channel: str = os.getenv("ATT_NOTIFY_CHANNEL", "log")
    notify_to_phone: str = os.getenv("ATT_NOTIFY_TO_PHONE", "+919876543210")
    notify_to_whatsapp: str = os.getenv("ATT_NOTIFY_TO_WHATSAPP", "whatsapp:+919876543210")
    twilio_account_sid: str = os.getenv("ATT_TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("ATT_TWILIO_AUTH_TOKEN", "")
    twilio_from_sms: str = os.getenv("ATT_TWILIO_FROM_SMS", "")
    twilio_from_whatsapp: str = os.getenv("ATT_TWILIO_FROM_WHATSAPP", "")


settings = Settings()
