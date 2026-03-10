import argparse

from cctv_daemon import execute_60_minute_period


def run_period_monitoring(
    class_id: str,
    duration_minutes: int,
    checks_count: int,
    threshold: float,
    min_instances: int,
    seconds_per_minute: float,
) -> int:
    """
    Backward-compatible entry point.
    Internally this now delegates to the strict 7-point CCTV daemon logic:
    60 min (10 + 40 + 10), randomized targeted twice verification, final posting.
    """
    return execute_60_minute_period(
        class_id=class_id,
        faculty_id="FACULTY_01",
        subject_code="MANUAL",
        subject_name="Manual Trigger",
        location_type="CLASSROOM",
        location_name=f"{class_id}-ROOM",
        camera_index=0,
        slot_label="MANUAL-PERIOD-LOGIC",
        timetable_id=None,
        test_mode=True,
        seconds_per_minute=seconds_per_minute,
    )


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run attendance period using strict daemon policy."
    )
    parser.add_argument("--class-id", required=True)
    parser.add_argument("--duration", type=int, default=60, help="Ignored: strict policy uses 60.")
    parser.add_argument("--checks", type=int, default=2, help="Ignored: strict policy uses 2 checks/student.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Ignored by strict policy config.")
    parser.add_argument("--min-instances", type=int, default=1, help="Ignored by strict policy config.")
    parser.add_argument("--sec-per-min", type=float, default=1.0)
    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    run_period_monitoring(
        class_id=args.class_id,
        duration_minutes=args.duration,
        checks_count=args.checks,
        threshold=args.threshold,
        min_instances=args.min_instances,
        seconds_per_minute=args.sec_per_min,
    )
