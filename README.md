# 🎓 Student Result Management System
Created a student grade managment system for my DBMS project which includes a functional database with marks ,email ,class, section and phone number  linked that with a python code to display edit and update database 


## 📁 Project Structure

```
student-result-management/
│
├── student_db.sql     # MySQL schema — tables, view, and sample data
├── db_config.py       # Database connection configuration
├── main.py            # Main CLI application
└── README.md
```

---

## 🗄️ Database Design

The system uses **4 database objects** inside `student_db`:

| Object | Type | Description |
|---|---|---|
| `students` | Table | Stores student personal info |
| `subjects` | Table | Stores subject names, max & pass marks |
| `marks` | Table | Stores marks per student per subject |
| `result_summary` | VIEW | Auto-calculates percentage, grade & pass/fail |

### Entity Relationship

```
students ──< marks >── subjects
                │
          result_summary (VIEW)
```

`marks` is a junction table linking students and subjects, with a composite unique key on `(student_id, subject_id, exam_type)` to prevent duplicate entries.

---

## ✨ Features

- ✅ Add, view, update, and delete student records
- ✅ Enter and update marks per subject per exam type (Final / Mid-term / Unit)
- ✅ Auto-calculated result summary via SQL VIEW — no manual computation
- ✅ Grade assigned automatically (A+ to F) based on percentage
- ✅ Strict pass/fail — fails if below pass marks in **any** subject
- ✅ Class topper leaderboard
- ✅ Subject-wise statistics (average, highest, lowest, pass count)
- ✅ Manage subjects dynamically (add new ones anytime)
- ✅ Sample data included for immediate testing

---

## 🧮 Grading Scale

| Percentage | Grade |
|---|---|
| 90 – 100 | A+ |
| 80 – 89  | A  |
| 70 – 79  | B  |
| 60 – 69  | C  |
| 33 – 59  | D  |
| Below 33 | F  |

> ⚠️ A student is marked **FAIL** if they score below `pass_marks` in even one subject, regardless of overall percentage.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Database | MySQL 8.x |
| DB Client | MySQL Workbench |
| Backend | Python 3.x |
| DB Connector | mysql-connector-python |
| Interface | Terminal / CLI |
| Editor | VS Code |

---

## ⚙️ Setup & Installation

### Prerequisites
- [MySQL](https://dev.mysql.com/downloads/) + MySQL Workbench installed
- [Python 3.x](https://www.python.org/downloads/) installed
- [VS Code](https://code.visualstudio.com/) (recommended)


## 🧪 Testing with Sample Data

The SQL script includes 4 sample students and marks across 5 subjects. To verify everything works right after setup:

- Press `7` → view full result summary with grades
- Press `8` → see the class topper list
- Press `9` → view subject-wise statistics

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `pip is not recognized` | Use `pip3 install mysql-connector-python` |
| `[DB ERROR] Could not connect` | Check your password in `db_config.py`; ensure MySQL is running |
| `Table already exists` warning | Safe to ignore — or re-run `student_db.sql` (it drops tables first) |
| `python is not recognized` | Use `python3 main.py` instead |

---

## 📚 Concepts Demonstrated

This project covers the following database and programming concepts:

- Relational database design with primary & foreign keys
- `ON DELETE CASCADE` for referential integrity
- SQL `VIEW` for computed result summaries
- `ON DUPLICATE KEY UPDATE` for upsert operations
- Python–MySQL integration using a connector
- Modular code structure (config, logic, UI separated)
- CLI menu-driven interface

---
