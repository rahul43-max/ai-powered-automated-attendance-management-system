import argparse

from database import get_class_students, sync_class_roster
from roster import load_roster_from_folders


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load fixed-class roster from data/known_faces.")
    parser.add_argument("--class-id", required=True, help="Class ID for enrolled students")
    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    students = load_roster_from_folders(args.class_id)
    if not students:
        raise SystemExit("No folders found under data/known_faces.")
    sync_class_roster(args.class_id, students)
    rows = get_class_students(args.class_id)
    print(f"Roster upsert complete: {len(rows)} students in class '{args.class_id}'.")
    for r in rows:
        print(f" - {r['student_id']} {r['full_name']}")
