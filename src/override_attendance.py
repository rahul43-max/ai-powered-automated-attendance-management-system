import argparse

from database import apply_override, get_final_attendance


def show_period(period_id: int) -> None:
    rows = get_final_attendance(period_id)
    if not rows:
        print("No final attendance found for this period.")
        return
    print(f"Period {period_id} attendance:")
    for row in rows:
        print(
            f"{row['student_id']} {row['full_name']} | "
            f"AI={row['ai_status']} | FINAL={row['final_status']} | "
            f"seen={row['detections_count']}/{row['checks_count']}"
        )


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lecturer manual override for period attendance.")
    parser.add_argument("--period-id", type=int, required=True)
    parser.add_argument("--student-id", type=str, help="Student ID to override")
    parser.add_argument("--status", choices=["PRESENT", "ABSENT"], help="New final status")
    parser.add_argument("--lecturer", type=str, default="unknown_lecturer")
    parser.add_argument("--reason", type=str, default="")
    parser.add_argument("--show-only", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    if args.show_only:
        show_period(args.period_id)
    else:
        if not args.student_id or not args.status:
            raise SystemExit("For override, provide --student-id and --status.")
        apply_override(
            period_id=args.period_id,
            student_id=args.student_id,
            new_status=args.status,
            lecturer=args.lecturer,
            reason=args.reason,
        )
        print("Override saved.")
        show_period(args.period_id)
