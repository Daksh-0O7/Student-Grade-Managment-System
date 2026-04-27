-- ============================================================
--  Student Result Management System — MySQL Schema
--  Run this file in MySQL Workbench:
--    File > Open SQL Script > student_db.sql > Execute (⚡)
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- ─────────────────────────────────────────
--  Table 1: students
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    student_id   INT AUTO_INCREMENT PRIMARY KEY,
    roll_no      VARCHAR(20)  NOT NULL UNIQUE,
    name         VARCHAR(100) NOT NULL,
    class        VARCHAR(20)  NOT NULL,
    section      CHAR(1)      NOT NULL,
    dob          DATE,
    email        VARCHAR(100),
    phone        VARCHAR(15),
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
--  Table 2: subjects
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS subjects (
    subject_id   INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20)  NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    max_marks    INT          NOT NULL DEFAULT 100,
    pass_marks   INT          NOT NULL DEFAULT 33
);

-- ─────────────────────────────────────────
--  Table 3: marks
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS marks (
    mark_id      INT AUTO_INCREMENT PRIMARY KEY,
    student_id   INT NOT NULL,
    subject_id   INT NOT NULL,
    marks_obtained DECIMAL(5,2) NOT NULL DEFAULT 0,
    exam_type    VARCHAR(30)  DEFAULT 'Final',
    entered_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE KEY unique_mark (student_id, subject_id, exam_type)
);

-- ─────────────────────────────────────────
--  Table 4: result_summary  (auto-calculated view)
-- ─────────────────────────────────────────
CREATE OR REPLACE VIEW result_summary AS
SELECT
    s.student_id,
    s.roll_no,
    s.name,
    s.class,
    s.section,
    COUNT(m.mark_id)                         AS total_subjects,
    SUM(m.marks_obtained)                    AS total_marks,
    SUM(sub.max_marks)                       AS max_possible,
    ROUND(SUM(m.marks_obtained) / SUM(sub.max_marks) * 100, 2) AS percentage,
    CASE
        WHEN SUM(m.marks_obtained) / SUM(sub.max_marks) * 100 >= 90 THEN 'A+'
        WHEN SUM(m.marks_obtained) / SUM(sub.max_marks) * 100 >= 80 THEN 'A'
        WHEN SUM(m.marks_obtained) / SUM(sub.max_marks) * 100 >= 70 THEN 'B'
        WHEN SUM(m.marks_obtained) / SUM(sub.max_marks) * 100 >= 60 THEN 'C'
        WHEN SUM(m.marks_obtained) / SUM(sub.max_marks) * 100 >= 33 THEN 'D'
        ELSE 'F'
    END AS grade,
    IF(
        MIN(m.marks_obtained - sub.pass_marks) >= 0,
        'PASS', 'FAIL'
    )                                        AS result
FROM students s
JOIN marks   m   ON s.student_id = m.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
GROUP BY s.student_id, s.roll_no, s.name, s.class, s.section;

-- ─────────────────────────────────────────
--  Sample data
-- ─────────────────────────────────────────
INSERT INTO subjects (subject_code, subject_name, max_marks, pass_marks) VALUES
('MATH101', 'Mathematics',       100, 33),
('ENG101',  'English',           100, 33),
('SCI101',  'Science',           100, 33),
('SST101',  'Social Studies',    100, 33),
('CS101',   'Computer Science',  100, 33);

INSERT INTO students (roll_no, name, class, section, dob, email) VALUES
('S001', 'Arjun Sharma',   '10', 'A', '2007-04-15', 'arjun@example.com'),
('S002', 'Priya Patel',    '10', 'A', '2007-08-22', 'priya@example.com'),
('S003', 'Ravi Kumar',     '10', 'B', '2007-01-10', 'ravi@example.com'),
('S004', 'Sneha Gupta',    '10', 'B', '2007-11-03', 'sneha@example.com');

INSERT INTO marks (student_id, subject_id, marks_obtained, exam_type) VALUES
(1, 1, 88, 'Final'), (1, 2, 76, 'Final'), (1, 3, 91, 'Final'), (1, 4, 83, 'Final'), (1, 5, 95, 'Final'),
(2, 1, 72, 'Final'), (2, 2, 85, 'Final'), (2, 3, 69, 'Final'), (2, 4, 78, 'Final'), (2, 5, 88, 'Final'),
(3, 1, 45, 'Final'), (3, 2, 55, 'Final'), (3, 3, 38, 'Final'), (3, 4, 50, 'Final'), (3, 5, 60, 'Final'),
(4, 1, 30, 'Final'), (4, 2, 40, 'Final'), (4, 3, 28, 'Final'), (4, 4, 35, 'Final'), (4, 5, 45, 'Final');

SELECT 'Database setup complete!' AS status;
