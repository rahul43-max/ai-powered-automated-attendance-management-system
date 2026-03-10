from database import (
    create_period,
    end_period,
    get_final_attendance,
    get_class_students,
    get_conn,
    insert_check,
    insert_detections,
    upsert_students,
    write_final_row,
)


def finalize_period(period_id: int, class_id: str, checks_count: int, threshold: float, min_instances: int) -> None:
    students = get_class_students(class_id)
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


def run_simulation() -> int:
    class_id = "SIM-CSE-A-2026"
    checks_count = 4
    threshold = 0.75
    min_instances = 2

    # Fixed enrolled class for simulation.
    students = [
        ("23R91A05L6", "Nithish Kumar", class_id),
        ("23R91A05P1", "Rahul P", class_id),
        ("23R91A05Q2", "Harshitha P", class_id),
        ("23R91A05R2", "Charan Kumar", class_id),
        ("23R91A0599", "Bob Proxy", class_id),
    ]
    upsert_students(students)

    period_id = create_period(
        class_id=class_id,
        duration_minutes=45,
        checks_count=checks_count,
        presence_threshold=threshold,
        min_instances_required=min_instances,
    )

    # Check plan mirrors your explanation:
    # - Bob appears once (proxy attempt) -> ABSENT.
    # - Rahul appears in 3/4 (late entry style) -> PRESENT at 75%.
    # - Harshitha appears in 3/4 (short break) -> PRESENT at 75%.
    # - Charan appears 0/4 (hidden/occlusion) -> ABSENT unless lecturer overrides.
    check_minutes = [12, 28, 41, 49]
    per_check_detections = [
        [("23R91A05L6_Nithish_Kumar", 0.21), ("23R91A05Q2_Harshitha_P", 0.24), ("23R91A0599_Bob_Proxy", 0.19)],
        [("23R91A05L6_Nithish_Kumar", 0.23), ("23R91A05P1_Rahul_P", 0.27), ("23R91A05Q2_Harshitha_P", 0.25)],
        [("23R91A05L6_Nithish_Kumar", 0.20), ("23R91A05P1_Rahul_P", 0.26)],
        [("23R91A05L6_Nithish_Kumar", 0.22), ("23R91A05P1_Rahul_P", 0.24), ("23R91A05Q2_Harshitha_P", 0.28)],
    ]

    for idx, minute in enumerate(check_minutes, start=1):
        check_id = insert_check(period_id, idx, minute, f"sim-check-{idx}")
        sid_and_dist = []
        for folder_label, dist in per_check_detections[idx - 1]:
            student_id = folder_label.split("_", 1)[0]
            sid_and_dist.append((student_id, dist))
        insert_detections(period_id, check_id, sid_and_dist)

    finalize_period(period_id, class_id, checks_count, threshold, min_instances)
    end_period(period_id)
    return period_id


if __name__ == "__main__":
    pid = run_simulation()
    print(f"Simulation completed. period_id={pid}")
    for row in get_final_attendance(pid):
        print(
            f"{row['student_id']} {row['full_name']} | "
            f"{row['detections_count']}/{row['checks_count']} ({row['detection_ratio']:.0%}) | "
            f"AI={row['ai_status']} | FINAL={row['final_status']}"
        )
