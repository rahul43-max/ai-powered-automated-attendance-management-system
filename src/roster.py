from pathlib import Path


KNOWN_FACES_DIR = Path("data/known_faces")


def parse_folder_name(folder_name: str) -> tuple[str, str]:
    # Expected: <student_id>_<full_name_with_underscores>
    if "_" not in folder_name:
        raise ValueError(
            f"Invalid folder name '{folder_name}'. Expected format: <student_id>_<full_name>"
        )
    student_id, full_name = folder_name.split("_", 1)
    return student_id, full_name.replace("_", " ")


def load_roster_from_folders(class_id: str) -> list[tuple[str, str, str]]:
    if not KNOWN_FACES_DIR.exists():
        return []
    students: list[tuple[str, str, str]] = []
    for path in sorted(KNOWN_FACES_DIR.iterdir()):
        if not path.is_dir():
            continue
        sid, name = parse_folder_name(path.name)
        students.append((sid, name, class_id))
    return students
