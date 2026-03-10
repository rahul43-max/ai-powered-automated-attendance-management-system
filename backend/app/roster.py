from pathlib import Path

from .settings import settings


def parse_folder_name(folder_name: str) -> tuple[str, str]:
    if "_" not in folder_name:
        raise ValueError(f"Invalid folder name: {folder_name}")
    student_id, full_name = folder_name.split("_", 1)
    return student_id, full_name.replace("_", " ")


def load_roster_for_class(class_id: str) -> list[tuple[str, str, str]]:
    root = Path(settings.known_faces_dir)
    if not root.exists():
        return []
    out: list[tuple[str, str, str]] = []
    for d in sorted(root.iterdir()):
        if d.is_dir():
            sid, name = parse_folder_name(d.name)
            out.append((sid, name, class_id))
    return out
