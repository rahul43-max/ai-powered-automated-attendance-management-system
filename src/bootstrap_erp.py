import argparse

from database import _utc_now, ensure_db, get_conn, replace_class_timetable


# Timings remain fixed semester-to-semester.
PERIOD_SLOTS = {
    1: ("09:40", "10:40"),
    2: ("10:40", "11:40"),
    3: ("11:40", "12:40"),
    4: ("13:20", "14:20"),
    5: ("14:20", "15:20"),
    6: ("15:20", "16:20"),
}


def _seed_users_and_students(class_id: str) -> None:
    now = _utc_now()
    with get_conn() as conn:
        # Faculty/staff users
        conn.execute(
            """
            INSERT INTO users(user_id, password_hash, role, full_name, phone_number, whatsapp_number)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                phone_number=excluded.phone_number,
                whatsapp_number=excluded.whatsapp_number
            """,
            ("FACULTY_01", "password", "staff", "Faculty Incharge 01", "+919876543210", "whatsapp:+919876543210"),
        )
        conn.execute(
            """
            INSERT INTO users(user_id, password_hash, role, full_name, phone_number, whatsapp_number)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                phone_number=excluded.phone_number,
                whatsapp_number=excluded.whatsapp_number
            """,
            ("FACULTY_02", "password", "staff", "Faculty Incharge 02", "+919876543211", "whatsapp:+919876543211"),
        )

        # Demo student login record
        conn.execute(
            """
            INSERT INTO users(user_id, password_hash, role, full_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO NOTHING
            """,
            ("23R91A05L6", "password", "student", "Mukkam Nithish Kumar"),
        )
        conn.execute(
            """
            INSERT INTO students(student_id, full_name, class_id, parent_phone, department, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                class_id=excluded.class_id,
                is_active=1
            """,
            ("23R91A05L6", "Mukkam Nithish Kumar", class_id, "9705874657", "CSE", now),
        )


def _semester_rows() -> list[tuple[str, int, str, str, str, str, str, str, str, int]]:
    """
    Row format:
    (day_of_week, period_number, start_time, end_time, subject_code,
     subject_name, faculty_id, location_type, location_name, camera_index)
    """
    # Example semester mapping. Subjects can be changed each semester;
    # slot timings are intentionally constant from PERIOD_SLOTS.
    plans = [
        ("Monday",    {1: ("ML", "Machine Learning", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       2: ("FLAT", "Formal Languages", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       3: ("SL", "Scripting Languages", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       4: ("FIOT", "Fundamentals of IoT", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       5: ("AI", "Artificial Intelligence", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       6: ("ML", "Machine Learning", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0)}),
        ("Tuesday",   {1: ("FLAT", "Formal Languages", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       2: ("SL", "Scripting Languages", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       3: ("AI", "Artificial Intelligence", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       4: ("FIOT", "Fundamentals of IoT", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       5: ("MLLAB", "Machine Learning Lab", "FACULTY_01", "LAB", "AI-LAB-2", 0),
                       6: ("MLLAB", "Machine Learning Lab", "FACULTY_01", "LAB", "AI-LAB-2", 0)}),
        ("Wednesday", {1: ("AILAB", "Artificial Intelligence Lab", "FACULTY_02", "LAB", "AI-LAB-1", 0),
                       2: ("AILAB", "Artificial Intelligence Lab", "FACULTY_02", "LAB", "AI-LAB-1", 0),
                       3: ("AILAB", "Artificial Intelligence Lab", "FACULTY_02", "LAB", "AI-LAB-1", 0),
                       4: ("SL", "Scripting Languages", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       5: ("AI", "Artificial Intelligence", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       6: ("FIOT", "Fundamentals of IoT", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0)}),
        ("Thursday",  {1: ("ML", "Machine Learning", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       2: ("FLAT", "Formal Languages", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       3: ("AI", "Artificial Intelligence", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       4: ("SLLAB", "Scripting Languages Lab", "FACULTY_02", "LAB", "SL-LAB-3", 0),
                       5: ("SLLAB", "Scripting Languages Lab", "FACULTY_02", "LAB", "SL-LAB-3", 0),
                       6: ("SLLAB", "Scripting Languages Lab", "FACULTY_02", "LAB", "SL-LAB-3", 0)}),
        ("Friday",    {1: ("FIOT", "Fundamentals of IoT", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       2: ("ML", "Machine Learning", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       3: ("AI", "Artificial Intelligence", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       4: ("FLAT", "Formal Languages", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       5: ("SL", "Scripting Languages", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       6: ("FIT", "Environmental Science", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0)}),
        ("Saturday",  {1: ("ML", "Machine Learning", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       2: ("AI", "Artificial Intelligence", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       3: ("SL", "Scripting Languages", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       4: ("FLAT", "Formal Languages", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       5: ("MENTOR", "Mentoring / Project Review", "FACULTY_01", "CLASSROOM", "CSE-D-ROOM-12", 0),
                       6: ("SPORT", "Activity / Sports", "FACULTY_02", "CLASSROOM", "CSE-D-ROOM-12", 0)}),
    ]

    rows: list[tuple[str, int, str, str, str, str, str, str, str, int]] = []
    for day_name, day_plan in plans:
        for period_no in range(1, 7):
            start_t, end_t = PERIOD_SLOTS[period_no]
            sub_code, sub_name, faculty_id, loc_type, loc_name, camera_index = day_plan[period_no]
            rows.append(
                (
                    day_name,
                    period_no,
                    start_t,
                    end_t,
                    sub_code,
                    sub_name,
                    faculty_id,
                    loc_type,
                    loc_name,
                    camera_index,
                )
            )
    return rows


def seed_erp(class_id: str, semester: str) -> None:
    ensure_db()
    _seed_users_and_students(class_id)
    replace_class_timetable(class_id, semester, _semester_rows())
    print(f"ERP bootstrap complete for class={class_id}, semester={semester}")
    print("Timings are fixed at 09:40,10:40,11:40,13:20,14:20,15:20 across all days.")
    print("Only subject/location mapping is semester-specific.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap ERP users + fixed-slot timetable.")
    parser.add_argument("--class-id", default="CSE-D", help="Class ID to seed.")
    parser.add_argument("--semester", default="2026-S2", help="Semester code (subjects can differ per semester).")
    args = parser.parse_args()
    seed_erp(class_id=args.class_id, semester=args.semester)
