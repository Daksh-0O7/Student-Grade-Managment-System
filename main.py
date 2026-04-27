# main.py  —  Student Result Management System
# ─────────────────────────────────────────────────────────────
#  Install dependency:  pip install mysql-connector-python
#  Run:                 python main.py
# ─────────────────────────────────────────────────────────────

from db_config import get_connection

# ════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════

def clear():
    print("\n" + "═" * 58)

def pause():
    input("\n  Press Enter to continue...")

def fmt_row(row, widths):
    return "  " + "  ".join(str(v).ljust(w) for v, w in zip(row, widths))

def print_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    sep = "  " + "  ".join("-" * w for w in widths)
    print(fmt_row(headers, widths))
    print(sep)
    for row in rows:
        print(fmt_row(row, widths))

# ════════════════════════════════════════════
#  STUDENT OPERATIONS
# ════════════════════════════════════════════

def add_student():
    clear()
    print("  ── Add New Student ──\n")
    roll   = input("  Roll No   : ").strip()
    name   = input("  Name      : ").strip()
    cls    = input("  Class     : ").strip()
    sec    = input("  Section   : ").strip().upper()
    dob    = input("  DOB (YYYY-MM-DD, or blank): ").strip() or None
    email  = input("  Email (or blank): ").strip() or None
    phone  = input("  Phone (or blank): ").strip() or None
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (roll_no, name, class, section, dob, email, phone) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (roll, name, cls, sec, dob, email, phone)
        )
        conn.commit()
        print(f"\n  ✔ Student '{name}' added (ID={cur.lastrowid})")
    except Exception as e:
        print(f"\n  ✘ Error: {e}")
    finally:
        conn.close()
    pause()

def view_students():
    clear()
    print("  ── All Students ──\n")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT student_id, roll_no, name, class, section, email FROM students ORDER BY roll_no")
        rows = cur.fetchall()
        if rows:
            print_table(["ID", "Roll No", "Name", "Class", "Sec", "Email"], rows)
        else:
            print("  No students found.")
    finally:
        conn.close()
    pause()

def update_student():
    clear()
    print("  ── Update Student ──\n")
    roll = input("  Enter Roll No to update: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT student_id, name, class, section, email, phone FROM students WHERE roll_no=%s", (roll,))
        row = cur.fetchone()
        if not row:
            print("  ✘ Roll No not found.")
            pause()
            return
        sid, name, cls, sec, email, phone = row
        print(f"\n  Current: {name} | Class {cls}-{sec} | {email} | {phone}")
        print("  (Leave blank to keep current value)\n")
        new_name  = input(f"  Name  [{name}]  : ").strip() or name
        new_cls   = input(f"  Class [{cls}]   : ").strip() or cls
        new_sec   = input(f"  Sec   [{sec}]   : ").strip().upper() or sec
        new_email = input(f"  Email [{email}] : ").strip() or email
        new_phone = input(f"  Phone [{phone}] : ").strip() or phone

        cur.execute(
            "UPDATE students SET name=%s, class=%s, section=%s, email=%s, phone=%s WHERE student_id=%s",
            (new_name, new_cls, new_sec, new_email, new_phone, sid)
        )
        conn.commit()
        print("\n  ✔ Student updated.")
    except Exception as e:
        print(f"\n  ✘ Error: {e}")
    finally:
        conn.close()
    pause()

def delete_student():
    clear()
    print("  ── Delete Student ──\n")
    roll = input("  Enter Roll No to delete: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT student_id, name FROM students WHERE roll_no=%s", (roll,))
        row = cur.fetchone()
        if not row:
            print("  ✘ Roll No not found.")
            pause()
            return
        sid, name = row
        confirm = input(f"  Delete '{name}' and ALL their marks? (yes/no): ").strip().lower()
        if confirm == "yes":
            cur.execute("DELETE FROM students WHERE student_id=%s", (sid,))
            conn.commit()
            print("  ✔ Student deleted.")
        else:
            print("  Cancelled.")
    except Exception as e:
        print(f"\n  ✘ Error: {e}")
    finally:
        conn.close()
    pause()

# ════════════════════════════════════════════
#  MARKS OPERATIONS
# ════════════════════════════════════════════

def add_marks():
    clear()
    print("  ── Enter Marks ──\n")
    roll = input("  Student Roll No: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT student_id, name FROM students WHERE roll_no=%s", (roll,))
        row = cur.fetchone()
        if not row:
            print("  ✘ Student not found.")
            pause()
            return
        sid, name = row
        print(f"\n  Entering marks for: {name}\n")

        cur.execute("SELECT subject_id, subject_code, subject_name, max_marks FROM subjects")
        subjects = cur.fetchall()
        exam_type = input("  Exam type (Final/Mid-term/Unit): ").strip() or "Final"

        for sub_id, code, sname, max_m in subjects:
            while True:
                try:
                    val = float(input(f"  {sname} ({code}) [max {max_m}]: "))
                    if 0 <= val <= max_m:
                        break
                    print(f"    Must be 0–{max_m}")
                except ValueError:
                    print("    Enter a number.")
            cur.execute(
                "INSERT INTO marks (student_id, subject_id, marks_obtained, exam_type) "
                "VALUES (%s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE marks_obtained=%s",
                (sid, sub_id, val, exam_type, val)
            )
        conn.commit()
        print("\n  ✔ Marks saved.")
    except Exception as e:
        print(f"\n  ✘ Error: {e}")
    finally:
        conn.close()
    pause()

def view_marks():
    clear()
    print("  ── Student Marks ──\n")
    roll = input("  Roll No (or blank for all): ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        if roll:
            cur.execute("""
                SELECT s.roll_no, s.name, sub.subject_name, m.marks_obtained, sub.max_marks, m.exam_type
                FROM marks m
                JOIN students s  ON m.student_id  = s.student_id
                JOIN subjects sub ON m.subject_id = sub.subject_id
                WHERE s.roll_no = %s
                ORDER BY sub.subject_name
            """, (roll,))
        else:
            cur.execute("""
                SELECT s.roll_no, s.name, sub.subject_name, m.marks_obtained, sub.max_marks, m.exam_type
                FROM marks m
                JOIN students s  ON m.student_id  = s.student_id
                JOIN subjects sub ON m.subject_id = sub.subject_id
                ORDER BY s.roll_no, sub.subject_name
            """)
        rows = cur.fetchall()
        if rows:
            print_table(["Roll", "Name", "Subject", "Marks", "Max", "Exam"], rows)
        else:
            print("  No marks found.")
    finally:
        conn.close()
    pause()

# ════════════════════════════════════════════
#  REPORTS
# ════════════════════════════════════════════

def result_report():
    clear()
    print("  ── Result Summary ──\n")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT roll_no, name, class, section,
                   total_subjects, total_marks, max_possible,
                   percentage, grade, result
            FROM result_summary
            ORDER BY roll_no
        """)
        rows = cur.fetchall()
        if rows:
            headers = ["Roll", "Name", "Cls", "Sec", "Subj", "Marks", "Max", "%", "Grade", "Result"]
            print_table(headers, rows)
        else:
            print("  No results yet. Enter marks first.")
    finally:
        conn.close()
    pause()

def topper_report():
    clear()
    print("  ── Class Toppers ──\n")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT roll_no, name, class, section, percentage, grade
            FROM result_summary
            ORDER BY percentage DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
        if rows:
            print_table(["Roll", "Name", "Class", "Sec", "Percentage", "Grade"], rows)
        else:
            print("  No data.")
    finally:
        conn.close()
    pause()

def subject_report():
    clear()
    print("  ── Subject-wise Average ──\n")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT sub.subject_name,
                   COUNT(m.mark_id)              AS students,
                   ROUND(AVG(m.marks_obtained),2) AS avg_marks,
                   MAX(m.marks_obtained)           AS highest,
                   MIN(m.marks_obtained)           AS lowest,
                   SUM(IF(m.marks_obtained >= sub.pass_marks,1,0)) AS passed
            FROM marks m
            JOIN subjects sub ON m.subject_id = sub.subject_id
            GROUP BY sub.subject_id, sub.subject_name
            ORDER BY avg_marks DESC
        """)
        rows = cur.fetchall()
        if rows:
            print_table(["Subject", "Students", "Avg", "Highest", "Lowest", "Passed"], rows)
        else:
            print("  No data.")
    finally:
        conn.close()
    pause()

def print_email_with_marks():
    clear()
    print("  ── Print Email with Marks ──\n")
    roll = input("  Student Roll No: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.name, s.email, sub.subject_name, m.marks_obtained, sub.max_marks
            FROM marks m
            JOIN students s  ON m.student_id  = s.student_id
            JOIN subjects sub ON m.subject_id = sub.subject_id
            WHERE s.roll_no = %s
            ORDER BY sub.subject_name
        """, (roll,))
        rows = cur.fetchall()
        if not rows:
            print("  ✘ Student or marks not found.")
            pause()
            return
        name, email = rows[0][0], rows[0][1]
        print(f"\n  To: {email}")
        print(f"  Subject: Marks Report for {name}\n")
        print_table(["Subject", "Marks", "Max"], [(r[2], r[3], r[4]) for r in rows])
        print("\n  (This is a simulation. No actual email sent.)")
    except Exception as e:
        print(f"\n  ✘ Error: {e}")
    finally:
        conn.close()
    pause()

# ════════════════════════════════════════════
#  SUBJECT MANAGEMENT
# ════════════════════════════════════════════

def manage_subjects():
    clear()
    print("  ── Subjects ──\n")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT subject_id, subject_code, subject_name, max_marks, pass_marks FROM subjects")
        rows = cur.fetchall()
        print_table(["ID", "Code", "Name", "Max", "Pass"], rows)
        print("\n  [A] Add subject   [B] Back")
        choice = input("\n  Choice: ").strip().upper()
        if choice == "A":
            code  = input("  Subject Code: ").strip()
            sname = input("  Subject Name: ").strip()
            mx    = int(input("  Max Marks [100]: ").strip() or 100)
            ps    = int(input("  Pass Marks [33]: ").strip() or 33)
            cur.execute(
                "INSERT INTO subjects (subject_code, subject_name, max_marks, pass_marks) VALUES (%s,%s,%s,%s)",
                (code, sname, mx, ps)
            )
            conn.commit()
            print("  ✔ Subject added.")
    except Exception as e:
        print(f"\n  ✘ Error: {e}")
    finally:
        conn.close()
    pause()

# ════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════

def main():
    while True:
        print("\n" + "═" * 58)
        print("   STUDENT RESULT MANAGEMENT SYSTEM")
        print("═" * 58)
        print("  STUDENTS")
        print("   1. Add student")
        print("   2. View all students")
        print("   3. Update student")
        print("   4. Delete student")
        print("\n  MARKS")
        print("   5. Enter / update marks")
        print("   6. View marks")
        print("\n  REPORTS")
        print("   7. Full result summary")
        print("   8. Class toppers")
        print("   9. Subject-wise report")
        print("\n  SETTINGS")
        print("  10. Manage subjects")
        print("  11. Print email with marks")
        print("   0. Exit")
        print("═" * 58)

        choice = input("  Enter choice: ").strip()

        actions = {
            "1": add_student,
            "2": view_students,
            "3": update_student,
            "4": delete_student,
            "5": add_marks,
            "6": view_marks,
            "7": result_report,
            "8": topper_report,
            "9": subject_report,
            "10": manage_subjects,
            "11":print_email_with_marks,
        }

        if choice == "0":
            print("\n  Goodbye!\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  Invalid option. Try again.")

if __name__ == "__main__":
    main()
