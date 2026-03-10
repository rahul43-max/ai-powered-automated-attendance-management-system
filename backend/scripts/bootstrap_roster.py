import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app import db
from app.roster import load_roster_for_class


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-id", required=True)
    args = parser.parse_args()

    roster = load_roster_for_class(args.class_id)
    if not roster:
        raise SystemExit("No roster folders found.")
    db.sync_class_roster(args.class_id, roster)
    print(f"synced class={args.class_id}, students={len(roster)}")
