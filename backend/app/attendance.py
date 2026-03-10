import random
import time
from datetime import datetime, timezone

from . import db
from .recognition import detect_known_students_once
from .roster import load_roster_for_class, parse_folder_name


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _schedule_checks(duration_minutes: int, checks_count: int) -> list[int]:
    if checks_count >= duration_minutes - 1:
        raise ValueError("checks_count must be smaller than duration_minutes - 1")
    out = random.sample(range(1, duration_minutes - 1), checks_count)
    out.sort()
    return out


def _finalize(period_id: int, class_id: str, checks_count: int, threshold: float, min_instances: int) -> None:
    students = db.get_class_students(class_id)
    logs = db.get_detection_logs(period_id)
    seen: dict[str, int] = {}
    for row in logs:
        sid = row["student_id"]
        seen[sid] = seen.get(sid, 0) + 1

    for s in students:
        sid = s["student_id"]
        cnt = seen.get(sid, 0)
        ratio = cnt / checks_count if checks_count else 0.0
        status = "PRESENT" if (cnt >= min_instances and ratio >= threshold) else "ABSENT"
        db.write_final_row(period_id, sid, cnt, checks_count, ratio, status)


def run_period(
    class_id: str,
    duration_minutes: int,
    checks_count: int,
    threshold: float,
    min_instances: int,
    seconds_per_minute: float,
) -> int:
    roster = load_roster_for_class(class_id)
    if not roster:
        raise RuntimeError("No enrolled students found in data/known_faces.")
    db.sync_class_roster(class_id, roster)

    period_id = db.create_period(class_id, duration_minutes, checks_count, threshold, min_instances)
    plan = _schedule_checks(duration_minutes, checks_count)

    print(f"\n[====] Period Started | period_id={period_id} | class_id={class_id} [====]")
    print(f"[*] Duration: {duration_minutes} min | Checks: {checks_count} | Threshold: {threshold:.0%}")
    print(f"[*] Min instances required: {min_instances}")
    print(f"[*] Random check minutes: {plan}")

    prev = 0
    for idx, minute in enumerate(plan, start=1):
        wait_sec = (minute - prev) * seconds_per_minute
        prev = minute
        if wait_sec > 0:
            time.sleep(wait_sec)
        print(f"\n[ALERT] Check {idx}/{checks_count} at period minute={minute}")
        check_id = db.insert_check(period_id, idx, minute, _utc_now())
        raw = detect_known_students_once()
        valid: list[tuple[str, float]] = []
        for folder_label, dist in raw:
            sid, _ = parse_folder_name(folder_label)
            valid.append((sid, dist))
        db.insert_detections(period_id, check_id, valid)
        if valid:
            detail = ", ".join([f"{sid} (d={dist:.3f})" for sid, dist in valid])
            print(f"    -> detected known students: {len(valid)} | {detail}")
        else:
            print("    -> detected known students: 0")

    _finalize(period_id, class_id, checks_count, threshold, min_instances)
    db.end_period(period_id)

    print("\n[====] Period Completed. Provisional AI Attendance [====]")
    for row in db.get_final_attendance(period_id):
        print(
            f"{row['student_id']} {row['full_name']} | "
            f"{row['detections_count']}/{row['checks_count']} ({row['detection_ratio']:.0%}) | "
            f"AI={row['ai_status']} | FINAL={row['final_status']}"
        )
    return period_id
