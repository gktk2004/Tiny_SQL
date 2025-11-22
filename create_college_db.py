import sqlite3

def create_database():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # =============================
    # CREATE TABLES
    # =============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Departments (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES Departments(department_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES Departments(department_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Enrollments (
            enrollment_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            course_id INTEGER,
            grade TEXT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            FOREIGN KEY (course_id) REFERENCES Courses(course_id)
        );
    """)

    # =============================
    # INSERT SAMPLE DATA
    # =============================

    cursor.executemany(
        "INSERT OR REPLACE INTO Departments VALUES (?, ?);",
        [
            (1, 'Computer Science'),
            (2, 'Mechanical Engineering'),
            (3, 'Electrical Engineering'),
        ]
    )

    cursor.executemany(
        "INSERT OR REPLACE INTO Students VALUES (?, ?, ?, ?);",
        [
            (1, 'John Doe', 20, 1),
            (2, 'Ananya Iyer', 21, 1),
            (3, 'Arjun Menon', 22, 2),
            (4, 'Sara Khan', 20, 3),
        ]
    )

    cursor.executemany(
        "INSERT OR REPLACE INTO Courses VALUES (?, ?, ?, ?);",
        [
            (101, 'Data Structures', 4, 1),
            (102, 'Operating Systems', 3, 1),
            (201, 'Thermodynamics', 4, 2),
            (202, 'Fluid Mechanics', 3, 2),
            (301, 'Circuit Analysis', 4, 3),
        ]
    )

    cursor.executemany(
        "INSERT OR REPLACE INTO Enrollments VALUES (?, ?, ?, ?);",
        [
            (1, 1, 101, 'A'),
            (2, 1, 102, 'B'),
            (3, 2, 101, 'A'),
            (4, 3, 201, 'B'),
            (5, 3, 202, 'A'),
            (6, 4, 301, 'A'),
        ]
    )

    conn.commit()
    conn.close()
    print("🎉 college.db created successfully!")


if __name__ == "__main__":
    create_database()
