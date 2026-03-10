import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .settings import settings


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_db() -> None:
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(settings.db_path) as conn:
        conn.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                class_id TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS periods (
                period_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                duration_minutes INTEGER NOT NULL,
                checks_count INTEGER NOT NULL,
                presence_threshold REAL NOT NULL,
                min_instances_required INTEGER NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS period_checks (
                check_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                check_index INTEGER NOT NULL,
                scheduled_minute INTEGER NOT NULL,
                actual_ts TEXT,
                FOREIGN KEY(period_id) REFERENCES periods(period_id)
            );

            CREATE TABLE IF NOT EXISTS detection_logs (
                detection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_id INTEGER NOT NULL,
                check_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                confidence_distance REAL NOT NULL,
                detected_ts TEXT NOT NULL,
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


def sync_class_roster(class_id: str, students: Iterable[tuple[str, str, str]]) -> None:
    rows = list(students)
    now = utc_now()
    with get_conn() as conn:
        conn.executemany(
            """
            INSERT INTO students(student_id, full_name, class_id, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                full_name=excluded.full_name,
                class_id=excluded.class_id,
                is_active=1
            """,
            [(sid, name, class_id, now) for sid, name, class_id in rows],
        )
        allowed = {sid for sid, _, _ in rows}
        existing = conn.execute(
            "SELECT student_id FROM students WHERE class_id=?",
            (class_id,),
        ).fetchall()
        for row in existing:
            sid = row["student_id"]
            if sid not in allowed:
                conn.execute(
                    "UPDATE students SET is_active=0 WHERE class_id=? AND student_id=?",
                    (class_id, sid),
                )


def list_classes() -> list[str]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT class_id FROM students WHERE is_active=1 ORDER BY class_id"
        ).fetchall()
    return [r["class_id"] for r in rows]


def get_class_students(class_id: str) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT student_id, full_name, class_id
            FROM students
            WHERE class_id=? AND is_active=1
            ORDER BY student_id
            """,
            (class_id,),
        ).fetchall()


def create_period(
    class_id: str,
    duration_minutes: int,
    checks_count: int,
    threshold: float,
    min_instances: int,
) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO periods(
                class_id, started_at, duration_minutes, checks_count,
                presence_threshold, min_instances_required, status
            ) VALUES (?, ?, ?, ?, ?, ?, 'running')
            """,
            (class_id, utc_now(), duration_minutes, checks_count, threshold, min_instances),
        )
        return int(cur.lastrowid)


def end_period(period_id: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE periods SET ended_at=?, status='completed' WHERE period_id=?",
            (utc_now(), period_id),
        )


def list_periods(limit: int = 50) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM periods ORDER BY period_id DESC LIMIT ?",
            (limit,),
        ).fetchall()


def get_period(period_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM periods WHERE period_id=?", (period_id,)).fetchone()


def insert_check(period_id: int, idx: int, scheduled_minute: int, actual_ts: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO period_checks(period_id, check_index, scheduled_minute, actual_ts)
            VALUES (?, ?, ?, ?)
            """,
            (period_id, idx, scheduled_minute, actual_ts),
        )
        return int(cur.lastrowid)


def get_period_checks(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT check_id, check_index, scheduled_minute, actual_ts
            FROM period_checks
            WHERE period_id=?
            ORDER BY check_index
            """,
            (period_id,),
        ).fetchall()


def insert_detections(period_id: int, check_id: int, rows: Iterable[tuple[str, float]]) -> None:
    data = [(period_id, check_id, sid, dist, utc_now()) for sid, dist in rows]
    if not data:
        return
    with get_conn() as conn:
        conn.executemany(
            """
            INSERT INTO detection_logs(period_id, check_id, student_id, confidence_distance, detected_ts)
            VALUES (?, ?, ?, ?, ?)
            """,
            data,
        )


def get_detection_logs(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT d.detection_id, d.period_id, d.check_id, d.student_id, s.full_name,
                   d.confidence_distance, d.detected_ts
            FROM detection_logs d
            JOIN students s ON s.student_id=d.student_id
            WHERE d.period_id=?
            ORDER BY d.check_id, d.student_id
            """,
            (period_id,),
        ).fetchall()


def write_final_row(
    period_id: int,
    student_id: str,
    detections_count: int,
    checks_count: int,
    ratio: float,
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
            (period_id, student_id, detections_count, checks_count, ratio, ai_status, ai_status, utc_now()),
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


def apply_override(period_id: int, student_id: str, new_status: str, lecturer: str, reason: str) -> None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT final_status FROM final_attendance WHERE period_id=? AND student_id=?",
            (period_id, student_id),
        ).fetchone()
        if row is None:
            raise ValueError("No final attendance row found for this student/period.")
        old_status = row["final_status"]
        conn.execute(
            "UPDATE final_attendance SET final_status=?, finalized_at=? WHERE period_id=? AND student_id=?",
            (new_status, utc_now(), period_id, student_id),
        )
        conn.execute(
            """
            INSERT INTO overrides(period_id, student_id, old_status, new_status, reason, lecturer, overridden_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (period_id, student_id, old_status, new_status, reason, lecturer, utc_now()),
        )


def get_overrides(period_id: int) -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT override_id, period_id, student_id, old_status, new_status, reason, lecturer, overridden_at
            FROM overrides
            WHERE period_id=?
            ORDER BY override_id DESC
            """,
            (period_id,),
        ).fetchall()
