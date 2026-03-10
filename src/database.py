import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional, Sequence

from config import settings


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {str(r[1]) for r in rows}


def _ensure_column(conn: sqlite3.Connection, table_name: str, column_name: str, definition: str) -> None:
    if column_name in _table_columns(conn, table_name):
        return
    conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def ensure_db() -> None:
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(settings.db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone_number TEXT,
                whatsapp_number TEXT
            );

            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                class_id TEXT NOT NULL,
                parent_phone TEXT,
                department TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS timetables (
                timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id TEXT NOT NULL,
                semester TEXT DEFAULT 'default',
                day_of_week TEXT NOT NULL,
                period_number INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                subject_code TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                faculty_id TEXT NOT NULL,
                location_type TEXT NOT NULL DEFAULT 'CLASSROOM',
                location_name TEXT NOT NULL DEFAULT 'ROOM-NA',
                camera_index INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(faculty_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS periods (
                period_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id TEXT NOT NULL,
                timetable_id INTEGER,
                subject_code TEXT,
                subject_name TEXT,
                faculty_id TEXT,
                location_type TEXT,
                location_name TEXT,
                camera_index INTEGER,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                attendance_posted_at TEXT,
                duration_minutes INTEGER NOT NULL,
                checks_count INTEGER NOT NULL,
                presence_threshold REAL NOT NULL,
                min_instances_required INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(timetable_id) REFERENCES timetables(timetable_id)
            );

            CREATE TABLE IF NOT EXISTS period_checks (
                check_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                check_index INTEGER NOT NULL,
                scheduled_minute INTEGER NOT NULL,
                actual_ts TEXT,
                target_student_id TEXT,
                phase TEXT NOT NULL DEFAULT 'ACTIVE',
                FOREIGN KEY(period_id) REFERENCES periods(period_id),
                FOREIGN KEY(target_student_id) REFERENCES students(student_id)
            );

            CREATE TABLE IF NOT EXISTS detection_logs (
                detection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                check_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                confidence_distance REAL NOT NULL,
                accuracy_score REAL NOT NULL DEFAULT 0.0,
                detected_ts TEXT NOT NULL,
                FOREIGN KEY(period_id) REFERENCES periods(period_id),
                FOREIGN KEY(check_id) REFERENCES period_checks(check_id),
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            );

            CREATE TABLE IF NOT EXISTS verification_attempts (
                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                check_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                scheduled_minute INTEGER NOT NULL,
                actual_ts TEXT NOT NULL,
                found INTEGER NOT NULL,
                best_distance REAL,
                best_accuracy REAL,
                min_required_accuracy REAL NOT NULL,
                detector_backend TEXT,
                model_name TEXT,
                camera_index INTEGER,
                notes TEXT,
                FOREIGN KEY(period_id) REFERENCES periods(period_id),
                FOREIGN KEY(check_id) REFERENCES period_checks(check_id),
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            );

            CREATE TABLE IF NOT EXISTS final_attendance (
                final_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                detections_count INTEGER NOT NULL,
                checks_count INTEGER NOT NULL,
                detection_ratio REAL NOT NULL,
                ai_status TEXT NOT NULL,
                final_status TEXT NOT NULL,
                finalized_at TEXT,
                UNIQUE(period_id, student_id),
                FOREIGN KEY(period_id) REFERENCES periods(period_id),
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            );

            CREATE TABLE IF NOT EXISTS overrides (
                override_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                old_status TEXT NOT NULL,
                new_status TEXT NOT NULL,
                reason TEXT,
                lecturer TEXT,
                overridden_at TEXT NOT NULL,
                FOREIGN KEY(period_id) REFERENCES periods(period_id),
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            );

            CREATE TABLE IF NOT EXISTS sms_logs (
                sms_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                student_id TEXT,
                phone_number TEXT NOT NULL,
                message TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                FOREIGN KEY(period_id) REFERENCES periods(period_id)
            );

            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                class_id TEXT NOT NULL,
                faculty_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                destination TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                FOREIGN KEY(period_id) REFERENCES periods(period_id),
                FOREIGN KEY(faculty_id) REFERENCES users(user_id)
            );
            """
        )

        # Migration-safe upgrades for pre-existing DBs.
        _ensure_column(conn, "users", "phone_number", "TEXT")
        _ensure_column(conn, "users", "whatsapp_number", "TEXT")
        _ensure_column(conn, "timetables", "semester", "TEXT DEFAULT 'default'")
        _ensure_column(conn, "timetables", "start_time", "TEXT NOT NULL DEFAULT '09:40'")
        _ensure_column(conn, "timetables", "end_time", "TEXT NOT NULL DEFAULT '10:40'")
        _ensure_column(conn, "timetables", "subject_code", "TEXT NOT NULL DEFAULT 'AUTO'")
        _ensure_column(conn, "timetables", "faculty_id", "TEXT NOT NULL DEFAULT 'FACULTY_01'")
        _ensure_column(conn, "timetables", "location_type", "TEXT NOT NULL DEFAULT 'CLASSROOM'")
        _ensure_column(conn, "timetables", "location_name", "TEXT NOT NULL DEFAULT 'ROOM-NA'")
        _ensure_column(conn, "timetables", "camera_index", "INTEGER NOT NULL DEFAULT 0")

        _ensure_column(conn, "periods", "subject_code", "TEXT")
        _ensure_column(conn, "periods", "subject_name", "TEXT")
        _ensure_column(conn, "periods", "faculty_id", "TEXT")
        _ensure_column(conn, "periods", "location_type", "TEXT")
        _ensure_column(conn, "periods", "location_name", "TEXT")
        _ensure_column(conn, "periods", "camera_index", "INTEGER")
        _ensure_column(conn, "periods", "attendance_posted_at", "TEXT")

        _ensure_column(conn, "period_checks", "target_student_id", "TEXT")
        _ensure_column(conn, "period_checks", "phase", "TEXT NOT NULL DEFAULT 'ACTIVE'")

        _ensure_column(conn, "detection_logs", "accuracy_score", "REAL NOT NULL DEFAULT 0.0")

        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_timetable_slot
            ON timetables(class_id, semester, day_of_week, period_number)
            """
        )


@contextmanager
def get_conn():
    ensure_db()
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def upsert_students(students: Iterable[tuple[str, str, str]]) -> None:
    now = _utc_now()
    with get_conn() as conn:
        for sid, name, class_id in students:
            conn.execute(
                """
                INSERT INTO users(user_id, password_hash, role, full_name)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    full_name=excluded.full_name
                """,
                (sid, "default_hash_tkrec", "student", name),
            )
            conn.execute(
                """
                INSERT INTO students(student_id, full_name, class_id, parent_phone, department, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    full_name=excluded.full_name,
                    class_id=excluded.class_id,
                    is_active=1
                """,
                (sid, name, class_id, "9000000000", "CSE", now),
            )


def set_user_contacts(user_id: str, phone_number: Optional[str], whatsapp_number: Optional[str]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE users
            SET phone_number=?, whatsapp_number=?
            WHERE user_id=?
            """,
            (phone_number, whatsapp_number, user_id),
        )


def get_user_contacts(user_id: str) -> tuple[Optional[str], Optional[str]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT phone_number, whatsapp_number FROM users WHERE user_id=?",
            (user_id,),
        ).fetchone()
    if row is None:
        return None, None
    return row["phone_number"], row["whatsapp_number"]


def sync_class_roster(class_id: str, students: Iterable[tuple[str, str, str]]) -> None:
    rows = list(students)
    upsert_students(rows)
    allowed_ids = {sid for sid, _, _ in rows}
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT student_id FROM students WHERE class_id=?",
            (class_id,),
        ).fetchall()
        for row in existing:
            sid = row["student_id"]
            if sid not in allowed_ids:
                conn.execute(
                    "UPDATE students SET is_active=0 WHERE class_id=? AND student_id=?",
                    (class_id, sid),
                )


def replace_class_timetable(
    class_id: str,
    semester: str,
    rows: Sequence[tuple[str, int, str, str, str, str, str, str, str, int]],
) -> None:
    """
    rows: (day_of_week, period_number, start_time, end_time, subject_code,
           subject_name, faculty_id, location_type, location_name, camera_index)
    """
    with get_conn() as conn:
        conn.execute("DELETE FROM timetables WHERE class_id=? AND semester=?", (class_id, semester))
        conn.executemany(
            """
            INSERT INTO timetables(
                class_id, semester, day_of_week, period_number, start_time, end_time,
                subject_code, subject_name, faculty_id, location_type, location_name, camera_index
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    class_id,
                    semester,
                    day,
                    period_no,
                    start_t,
                    end_t,
                    subject_code,
                    subject_name,
                    faculty_id,
                    location_type,
                    location_name,
                    camera_index,
                )
                for (
                    day,
                    period_no,
                    start_t,
                    end_t,
                    subject_code,
                    subject_name,
                    faculty_id,
                    location_type,
                    location_name,
                    camera_index,
                ) in rows
            ],
        )


def get_timetable_entries_for_slot(day_of_week: str, start_time: str) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT timetable_id, class_id, semester, day_of_week, period_number,
                   start_time, end_time, subject_code, subject_name, faculty_id,
                   location_type, location_name, camera_index
            FROM timetables
            WHERE day_of_week=? AND start_time=?
            ORDER BY class_id, period_number
            """,
            (day_of_week, start_time),
        ).fetchall()


def create_period(
    class_id: str,
    duration_minutes: int,
    checks_count: int,
    presence_threshold: float,
    min_instances_required: int,
    timetable_id: Optional[int] = None,
    subject_code: Optional[str] = None,
    subject_name: Optional[str] = None,
    faculty_id: Optional[str] = None,
    location_type: Optional[str] = None,
    location_name: Optional[str] = None,
    camera_index: Optional[int] = None,
) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO periods(
                class_id, timetable_id, subject_code, subject_name, faculty_id,
                location_type, location_name, camera_index,
                started_at, duration_minutes, checks_count, presence_threshold,
                min_instances_required, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                class_id,
                timetable_id,
                subject_code,
                subject_name,
                faculty_id,
                location_type,
                location_name,
                camera_index,
                _utc_now(),
                duration_minutes,
                checks_count,
                presence_threshold,
                min_instances_required,
                "running",
            ),
        )
        return int(cur.lastrowid)


def mark_period_attendance_posted(period_id: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE periods SET attendance_posted_at=? WHERE period_id=?",
            (_utc_now(), period_id),
        )


def end_period(period_id: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE periods SET ended_at=?, status='completed' WHERE period_id=?",
            (_utc_now(), period_id),
        )


def get_period(period_id: int) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM periods WHERE period_id=?", (period_id,)
        ).fetchone()


def list_periods(limit: int = 50) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT *
            FROM periods
            ORDER BY period_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()


def get_class_students(class_id: str) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT student_id, full_name, class_id, parent_phone, department
            FROM students
            WHERE class_id=? AND is_active=1
            ORDER BY student_id
            """,
            (class_id,),
        ).fetchall()


def list_classes() -> list[str]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT DISTINCT class_id
            FROM students
            WHERE is_active=1
            ORDER BY class_id
            """
        ).fetchall()
        return [r["class_id"] for r in rows]


def insert_check(
    period_id: int,
    check_index: int,
    scheduled_minute: int,
    actual_ts: str,
    target_student_id: Optional[str] = None,
    phase: str = "ACTIVE",
) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO period_checks(
                period_id, check_index, scheduled_minute, actual_ts, target_student_id, phase
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (period_id, check_index, scheduled_minute, actual_ts, target_student_id, phase),
        )
        return int(cur.lastrowid)


def get_period_checks(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT check_id, check_index, scheduled_minute, actual_ts, target_student_id, phase
            FROM period_checks
            WHERE period_id=?
            ORDER BY check_index
            """,
            (period_id,),
        ).fetchall()


def _distance_to_accuracy(distance: float) -> float:
    dist = max(0.0, min(1.0, float(distance)))
    return round((1.0 - dist) * 100.0, 4)


def insert_detections(period_id: int, check_id: int, detections: Iterable[tuple]) -> None:
    rows: list[tuple[int, int, str, float, float, str]] = []
    detected_ts = _utc_now()
    for item in detections:
        if len(item) == 3:
            sid, dist, accuracy = item  # type: ignore[misc]
            dist_f = float(dist)
            acc_f = float(accuracy)
        elif len(item) == 2:
            sid, dist = item  # type: ignore[misc]
            dist_f = float(dist)
            acc_f = _distance_to_accuracy(dist_f)
        else:
            continue
        rows.append((period_id, check_id, str(sid), dist_f, acc_f, detected_ts))

    if not rows:
        return

    with get_conn() as conn:
        conn.executemany(
            """
            INSERT INTO detection_logs(
                period_id, check_id, student_id, confidence_distance, accuracy_score, detected_ts
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )


def get_detection_logs(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT d.detection_id, d.period_id, d.check_id, d.student_id, s.full_name,
                   d.confidence_distance, d.accuracy_score, d.detected_ts
            FROM detection_logs d
            JOIN students s ON s.student_id = d.student_id
            WHERE d.period_id=?
            ORDER BY d.check_id, d.student_id
            """,
            (period_id,),
        ).fetchall()


def log_verification_attempt(
    period_id: int,
    check_id: int,
    student_id: str,
    scheduled_minute: int,
    found: bool,
    best_distance: Optional[float],
    best_accuracy: Optional[float],
    min_required_accuracy: float,
    detector_backend: str,
    model_name: str,
    camera_index: int,
    notes: str = "",
    actual_ts: Optional[str] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO verification_attempts(
                period_id, check_id, student_id, scheduled_minute, actual_ts, found,
                best_distance, best_accuracy, min_required_accuracy, detector_backend,
                model_name, camera_index, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                period_id,
                check_id,
                student_id,
                scheduled_minute,
                actual_ts or _utc_now(),
                1 if found else 0,
                best_distance,
                best_accuracy,
                min_required_accuracy,
                detector_backend,
                model_name,
                camera_index,
                notes,
            ),
        )


def get_verification_attempts(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT attempt_id, period_id, check_id, student_id, scheduled_minute, actual_ts,
                   found, best_distance, best_accuracy, min_required_accuracy,
                   detector_backend, model_name, camera_index, notes
            FROM verification_attempts
            WHERE period_id=?
            ORDER BY attempt_id
            """,
            (period_id,),
        ).fetchall()


def write_final_row(
    period_id: int,
    student_id: str,
    detections_count: int,
    checks_count: int,
    detection_ratio: float,
    ai_status: str,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO final_attendance(
                period_id, student_id, detections_count, checks_count, detection_ratio,
                ai_status, final_status, finalized_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(period_id, student_id) DO UPDATE SET
                detections_count=excluded.detections_count,
                checks_count=excluded.checks_count,
                detection_ratio=excluded.detection_ratio,
                ai_status=excluded.ai_status,
                final_status=excluded.final_status,
                finalized_at=excluded.finalized_at
            """,
            (
                period_id,
                student_id,
                detections_count,
                checks_count,
                detection_ratio,
                ai_status,
                ai_status,
                _utc_now(),
            ),
        )


def get_final_attendance(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT f.*, s.full_name
            FROM final_attendance f
            JOIN students s ON s.student_id=f.student_id
            WHERE f.period_id=?
            ORDER BY s.student_id
            """,
            (period_id,),
        ).fetchall()


def get_overrides(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT override_id, period_id, student_id, old_status, new_status,
                   reason, lecturer, overridden_at
            FROM overrides
            WHERE period_id=?
            ORDER BY override_id DESC
            """,
            (period_id,),
        ).fetchall()


def apply_override(
    period_id: int,
    student_id: str,
    new_status: str,
    lecturer: str,
    reason: str = "",
) -> None:
    status = new_status.upper().strip()
    if status not in {"PRESENT", "ABSENT"}:
        raise ValueError("new_status must be PRESENT or ABSENT.")

    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT final_status FROM final_attendance
            WHERE period_id=? AND student_id=?
            """,
            (period_id, student_id),
        ).fetchone()
        if row is None:
            raise ValueError("No final attendance row found for this student/period.")
        old_status = row["final_status"]
        conn.execute(
            """
            UPDATE final_attendance
            SET final_status=?, finalized_at=?
            WHERE period_id=? AND student_id=?
            """,
            (status, _utc_now(), period_id, student_id),
        )
        conn.execute(
            """
            INSERT INTO overrides(
                period_id, student_id, old_status, new_status,
                reason, lecturer, overridden_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (period_id, student_id, old_status, status, reason, lecturer, _utc_now()),
        )


def log_sms(period_id: int, student_id: str, phone: str, message: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO sms_logs(period_id, student_id, phone_number, message, sent_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (period_id, student_id, phone, message, _utc_now()),
        )


def get_sms_logs() -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM sms_logs ORDER BY sms_id DESC").fetchall()


def log_notification(
    period_id: int,
    class_id: str,
    faculty_id: str,
    channel: str,
    destination: str,
    message: str,
    status: str,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO notifications(
                period_id, class_id, faculty_id, channel, destination, message, status, sent_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (period_id, class_id, faculty_id, channel, destination, message, status, _utc_now()),
        )


def get_notifications(period_id: Optional[int] = None) -> list[sqlite3.Row]:
    with get_conn() as conn:
        if period_id is None:
            return conn.execute(
                "SELECT * FROM notifications ORDER BY notification_id DESC"
            ).fetchall()
        return conn.execute(
            "SELECT * FROM notifications WHERE period_id=? ORDER BY notification_id DESC",
            (period_id,),
        ).fetchall()


def get_period_status_counts(period_id: int) -> dict[str, int]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT final_status, COUNT(*) AS c
            FROM final_attendance
            WHERE period_id=?
            GROUP BY final_status
            """,
            (period_id,),
        ).fetchall()

    out = {"PRESENT": 0, "ABSENT": 0}
    for row in rows:
        key = str(row["final_status"]).upper()
        if key in out:
            out[key] = int(row["c"])
    return out


def auth_user(user_id: str, password_hash: str) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE user_id=? AND password_hash=?",
            (user_id, password_hash),
        ).fetchone()
