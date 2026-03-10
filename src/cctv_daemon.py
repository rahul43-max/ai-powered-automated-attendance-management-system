import argparse
import base64
import random
import time
from datetime import datetime, timezone
from typing import Optional
from urllib import parse, request

from config import settings
from database import (
    create_period,
    end_period,
    get_class_students,
    get_conn,
    get_period_status_counts,
    get_timetable_entries_for_slot,
    get_user_contacts,
    insert_check,
    log_notification,
    log_sms,
    mark_period_attendance_posted,
    set_user_contacts,
    sync_class_roster,
    write_final_row,
)
from roster import load_roster_from_folders
from targeted_ai_search import execute_random_class_sweep

CHECKS_PER_STUDENT = 2
TOTAL_PERIOD_MINUTES = 60
INITIAL_GRACE_MINUTES = 10
ACTIVE_START_MINUTE = 11
ACTIVE_END_MINUTE = 50
FIRST_CHECK_MIN_START = 11
FIRST_CHECK_MIN_END = 30
SECOND_CHECK_MIN_START = 31
SECOND_CHECK_MIN_END = 40
FINAL_GRACE_START_MINUTE = 51
POST_ATTENDANCE_MINUTE = 55
PRESENCE_THRESHOLD = 0.50
MIN_INSTANCES_REQUIRED = 1


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _upsert_faculty_user(
    faculty_id: str,
    faculty_name: Optional[str] = None,
    faculty_phone: Optional[str] = None,
    faculty_whatsapp: Optional[str] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO users(user_id, password_hash, role, full_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO NOTHING
            """,
            (faculty_id, "default_hash_tkrec", "staff", faculty_name or faculty_id),
        )
    if faculty_phone is not None or faculty_whatsapp is not None:
        set_user_contacts(faculty_id, faculty_phone, faculty_whatsapp)


def _sync_students_for_class(class_id: str) -> None:
    roster = load_roster_from_folders(class_id)
    if roster:
        sync_class_roster(class_id, roster)


def create_student_schedule(class_id: str) -> dict[int, list[str]]:
    """
    Each student is scheduled exactly twice in the 40-minute active window:
    - first random check in minutes 11-30
    - second random check in minutes 31-40
    """
    students = get_class_students(class_id)
    if not students:
        raise RuntimeError(f"No active students found for class {class_id}.")

    schedule: dict[int, list[str]] = {}
    attempts_per_student: dict[str, int] = {}
    for row in students:
        sid = row["student_id"]
        first_minute = random.randint(FIRST_CHECK_MIN_START, FIRST_CHECK_MIN_END)
        second_minute = random.randint(SECOND_CHECK_MIN_START, SECOND_CHECK_MIN_END)

        schedule.setdefault(first_minute, []).append(sid)
        schedule.setdefault(second_minute, []).append(sid)
        attempts_per_student[sid] = attempts_per_student.get(sid, 0) + 2

    for minute in schedule:
        random.shuffle(schedule[minute])  # randomized, non-sequential targeted scanning

    # Enforce exact twice-verification rule before runtime starts.
    for sid, count in attempts_per_student.items():
        if count != CHECKS_PER_STUDENT:
            raise RuntimeError(f"Scheduling error for {sid}: expected 2 checks, got {count}")

    return schedule


def finalize_period(period_id: int, class_id: str) -> None:
    students = get_class_students(class_id)
    checks_count = CHECKS_PER_STUDENT
    threshold = PRESENCE_THRESHOLD
    min_instances = MIN_INSTANCES_REQUIRED

    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT student_id, COUNT(*) AS seen_count
            FROM detection_logs
            WHERE period_id=?
            GROUP BY student_id
            """,
            (period_id,),
        ).fetchall()

    seen_map = {r["student_id"]: int(r["seen_count"]) for r in rows}
    for student in students:
        sid = student["student_id"]
        cnt = seen_map.get(sid, 0)
        ratio = cnt / checks_count if checks_count else 0.0
        status = "PRESENT" if (cnt >= min_instances and ratio >= threshold) else "ABSENT"
        write_final_row(period_id, sid, cnt, checks_count, ratio, status)


def _send_twilio_message(to_number: str, from_number: str, body: str) -> tuple[bool, str]:
    sid = settings.twilio_account_sid.strip()
    token = settings.twilio_auth_token.strip()
    if not sid or not token or not from_number:
        return False, "twilio_credentials_missing"

    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
        payload = parse.urlencode({"To": to_number, "From": from_number, "Body": body}).encode()
        req = request.Request(url, data=payload, method="POST")
        auth = base64.b64encode(f"{sid}:{token}".encode("ascii")).decode("ascii")
        req.add_header("Authorization", f"Basic {auth}")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with request.urlopen(req, timeout=15) as resp:
            if 200 <= resp.status < 300:
                return True, f"sent_http_{resp.status}"
            return False, f"twilio_http_{resp.status}"
    except Exception as exc:
        return False, f"twilio_error: {exc}"


def generate_faculty_notification(
    period_id: int,
    class_id: str,
    faculty_id: str,
    subject_name: str,
    slot_label: str,
) -> None:
    counts = get_period_status_counts(period_id)
    present_count = counts["PRESENT"]
    absent_count = counts["ABSENT"]
    total = present_count + absent_count

    message = (
        f"ATTENDANCE ALERT | Class {class_id} | {subject_name} | Slot {slot_label} | "
        f"Present: {present_count}/{total} | Absent: {absent_count}. "
        "Please review portal overrides if any student disputes attendance."
    )

    channel = settings.notify_channel.strip().lower()
    faculty_phone, faculty_whatsapp = get_user_contacts(faculty_id)
    destination = faculty_phone or settings.notify_to_phone
    status = "logged"

    if channel == "sms":
        destination = faculty_phone or settings.notify_to_phone
        log_sms(period_id, faculty_id, destination, message)
        status = "logged_sms"
    elif channel == "whatsapp":
        destination = faculty_whatsapp or settings.notify_to_whatsapp
        log_sms(period_id, faculty_id, destination, message)
        status = "logged_whatsapp"
    elif channel == "twilio_sms":
        destination = faculty_phone or settings.notify_to_phone
        ok, detail = _send_twilio_message(destination, settings.twilio_from_sms, message)
        if ok:
            log_sms(period_id, faculty_id, destination, message)
        status = detail
    elif channel == "twilio_whatsapp":
        destination = faculty_whatsapp or settings.notify_to_whatsapp
        ok, detail = _send_twilio_message(destination, settings.twilio_from_whatsapp, message)
        if ok:
            log_sms(period_id, faculty_id, destination, message)
        status = detail
    elif channel == "auto":
        destination = faculty_whatsapp or settings.notify_to_whatsapp
        ok, detail = _send_twilio_message(destination, settings.twilio_from_whatsapp, message)
        if not ok:
            destination = faculty_phone or settings.notify_to_phone
            ok, detail = _send_twilio_message(destination, settings.twilio_from_sms, message)
        if ok:
            log_sms(period_id, faculty_id, destination, message)
        status = detail
    else:
        channel = "log"

    log_notification(
        period_id=period_id,
        class_id=class_id,
        faculty_id=faculty_id,
        channel=channel,
        destination=destination,
        message=message,
        status=status,
    )
    print(f"[NOTIFY] {channel.upper()} -> {destination} ({status})")
    print(f"[NOTIFY] {message}")


def execute_60_minute_period(
    class_id: str,
    faculty_id: str,
    subject_code: str,
    subject_name: str,
    location_type: str,
    location_name: str,
    camera_index: int,
    slot_label: str,
    timetable_id: Optional[int] = None,
    test_mode: bool = False,
    seconds_per_minute: Optional[float] = None,
    faculty_phone: Optional[str] = None,
    faculty_whatsapp: Optional[str] = None,
) -> int:
    _sync_students_for_class(class_id)
    students = get_class_students(class_id)
    if not students:
        raise RuntimeError(
            f"No enrolled students available for class {class_id}. "
            "Capture student images, train model, and bootstrap roster first."
        )

    _upsert_faculty_user(
        faculty_id=faculty_id,
        faculty_phone=faculty_phone,
        faculty_whatsapp=faculty_whatsapp,
    )

    duration = TOTAL_PERIOD_MINUTES
    checks_per_student = CHECKS_PER_STUDENT
    threshold = PRESENCE_THRESHOLD
    min_instances = MIN_INSTANCES_REQUIRED

    period_id = create_period(
        class_id=class_id,
        duration_minutes=duration,
        checks_count=checks_per_student,
        presence_threshold=threshold,
        min_instances_required=min_instances,
        timetable_id=timetable_id,
        subject_code=subject_code,
        subject_name=subject_name,
        faculty_id=faculty_id,
        location_type=location_type,
        location_name=location_name,
        camera_index=camera_index,
    )
    schedule = create_student_schedule(class_id)
    total_target_checks = len(students) * checks_per_student

    if seconds_per_minute is not None:
        sec_per_min = seconds_per_minute
    else:
        sec_per_min = 1.0 if test_mode else settings.seconds_per_minute

    print("\n==========================================================")
    print("AI CCTV DAEMON | PERIOD STARTED")
    print("==========================================================")
    print(f"period_id={period_id} class={class_id} faculty={faculty_id}")
    print(f"subject={subject_code} {subject_name} | {location_type}:{location_name} | camera={camera_index}")
    print(f"slot={slot_label} | duration={duration} min | checks/student={checks_per_student}")
    print(
        f"policy: grace(1-{INITIAL_GRACE_MINUTES}), active({ACTIVE_START_MINUTE}-{ACTIVE_END_MINUTE}), "
        f"grace({FINAL_GRACE_START_MINUTE}-{TOTAL_PERIOD_MINUTES}), post at minute {POST_ATTENDANCE_MINUTE}"
    )
    print(f"planned targeted verifications={total_target_checks}")

    check_index = 0
    posted = False
    loop_start = time.time()

    for minute in range(1, duration + 1):
        target_seconds = minute * sec_per_min
        while True:
            elapsed = time.time() - loop_start
            if elapsed >= target_seconds:
                break
            time.sleep(0.05)

        if minute == 1:
            print("[GRACE] Initial 10-minute grace started. No monitoring.")

        # Active monitoring window: 11-50
        if ACTIVE_START_MINUTE <= minute <= ACTIVE_END_MINUTE:
            targets = schedule.get(minute, [])
            if targets:
                print(f"\n[ACTIVE] minute {minute}/60 | targeted checks={len(targets)}")
            for sid in targets:
                check_index += 1
                check_id = insert_check(
                    period_id=period_id,
                    check_index=check_index,
                    scheduled_minute=minute,
                    actual_ts=_utc_now(),
                    target_student_id=sid,
                    phase="ACTIVE",
                )
                result = execute_random_class_sweep(
                    period_id=period_id,
                    check_id=check_id,
                    scheduled_student_id=sid,
                    scheduled_minute=minute,
                    camera_index=camera_index,
                )
                if result["found"]:
                    print(
                        f"  [+] {sid} detected | acc={result['best_accuracy']:.2f}% "
                        f"| dist={result['best_distance']:.4f}"
                    )
                else:
                    reason = result.get("notes", "no_match")
                    print(f"  [-] {sid} not detected ({reason})")

        if minute == FINAL_GRACE_START_MINUTE:
            print("\n[GRACE] Final 10-minute grace started.")

        # Post attendance in last 5 minutes.
        if minute == POST_ATTENDANCE_MINUTE and not posted:
            print("\n[POST] Finalizing attendance and posting results...")
            finalize_period(period_id, class_id)
            mark_period_attendance_posted(period_id)
            generate_faculty_notification(
                period_id=period_id,
                class_id=class_id,
                faculty_id=faculty_id,
                subject_name=subject_name,
                slot_label=slot_label,
            )
            posted = True

    # Safety finalization if posting minute was skipped by custom configs.
    if not posted:
        finalize_period(period_id, class_id)
        mark_period_attendance_posted(period_id)
        generate_faculty_notification(
            period_id=period_id,
            class_id=class_id,
            faculty_id=faculty_id,
            subject_name=subject_name,
            slot_label=slot_label,
        )

    end_period(period_id)
    print("[DONE] Period completed and stored permanently.")
    return period_id


def run_daemon() -> None:
    parser = argparse.ArgumentParser(description="Autonomous timetable-driven CCTV attendance daemon")
    parser.add_argument("--test-run", action="store_true", help="Run one immediate 60-minute cycle in fast simulation.")
    parser.add_argument("--class-id", default="CSE-D", help="Class ID for test-run mode.")
    parser.add_argument("--faculty-id", default="FACULTY_01", help="Faculty ID for test-run mode.")
    parser.add_argument("--subject-code", default="AUTO", help="Subject code for test-run mode.")
    parser.add_argument("--subject-name", default="AUTO PERIOD", help="Subject name for test-run mode.")
    parser.add_argument("--location-type", default="CLASSROOM", help="CLASSROOM or LAB for test-run mode.")
    parser.add_argument("--location-name", default="ROOM-NA", help="Room/Lab name for test-run mode.")
    parser.add_argument("--camera-index", type=int, default=settings.camera_index, help="Camera index to monitor.")
    parser.add_argument("--faculty-phone", default=settings.notify_to_phone, help="Faculty SMS number for test-run mode.")
    parser.add_argument(
        "--faculty-whatsapp",
        default=settings.notify_to_whatsapp,
        help="Faculty WhatsApp number for test-run mode (e.g. whatsapp:+91...).",
    )
    parser.add_argument("--sec-per-min", type=float, default=None, help="Override seconds per simulated minute.")
    args = parser.parse_args()

    if args.test_run:
        print("==========================================================")
        print("CCTV DAEMON TEST RUN (REAL CAMERA PIPELINE)")
        print("==========================================================")
        execute_60_minute_period(
            class_id=args.class_id,
            faculty_id=args.faculty_id,
            subject_code=args.subject_code,
            subject_name=args.subject_name,
            location_type=args.location_type,
            location_name=args.location_name,
            camera_index=args.camera_index,
            slot_label="TEST-RUN",
            timetable_id=None,
            test_mode=True,
            seconds_per_minute=args.sec_per_min if args.sec_per_min is not None else 1.0,
            faculty_phone=args.faculty_phone,
            faculty_whatsapp=args.faculty_whatsapp,
        )
        return

    print("==========================================================")
    print("CCTV DAEMON INITIALIZED (REALTIME TIMETABLE MODE)")
    print("==========================================================")

    while True:
        now = datetime.now()
        day_name = now.strftime("%A")
        hhmm = now.strftime("%H:%M")

        due_entries = get_timetable_entries_for_slot(day_name, hhmm)
        if due_entries:
            # Sequential execution is intentional for one-machine/one-camera setups.
            for entry in due_entries:
                print(
                    f"\n[TIMETABLE MATCH] {day_name} {hhmm} -> "
                    f"class={entry['class_id']} period={entry['period_number']} "
                    f"{entry['subject_code']} {entry['subject_name']} "
                    f"{entry['location_type']}:{entry['location_name']}"
                )
                execute_60_minute_period(
                    class_id=entry["class_id"],
                    faculty_id=entry["faculty_id"],
                    subject_code=entry["subject_code"],
                    subject_name=entry["subject_name"],
                    location_type=entry["location_type"],
                    location_name=entry["location_name"],
                    camera_index=int(entry["camera_index"]),
                    slot_label=f"{entry['day_of_week']} {entry['start_time']}",
                    timetable_id=int(entry["timetable_id"]),
                    test_mode=False,
                    seconds_per_minute=None,
                    faculty_phone=None,
                    faculty_whatsapp=None,
                )

        time.sleep(max(5, settings.daemon_poll_seconds))


if __name__ == "__main__":
    run_daemon()
