TinySQL 
AI & Automation Internship Challenge Submission  
Author: GOUTHAM KRISHNA T K 
Task: Option 3 — Tiny SQL Expert (SLM Optimization)

Overview
TinySQL is a lightweight natural-language-to-SQL translator powered by the Phi-3 Mini (3.8B) Small Language Model (SLM) running locally via Ollama.
This system converts natural language questions into SQL queries for a custom College Database Schema, validates the SQL, performs automatic self-correction, and outputs only raw SQL, as required by the internship challenge.

Features

•	Natural language → SQL translation  
•	Understands a 4-table College DB schema  
•	Uses JOIN operations when needed  
•	Validates SQL (syntax + forbidden words)  
•	Self-correction loop for fixing model mistakes  
•	Works fully offline using local SLM  
•	Pure SQL output (no explanation text)



Database Schema (College DB)

Students Table
| Column        | Type    |
|---------------|---------|
| student_id      | INTEGER |
| name          | TEXT    |
| age           | INTEGER |
| department_id | INTEGER |

Departments Table
| Column         | Type    |
|----------------|---------|
| department_id  | INTEGER |
| department_name| TEXT    |

Courses Table
| Column         | Type    |
|----------------|---------|
| course_id      | INTEGER |
| course_name    | TEXT    |
| credits        | INTEGER |
| department_id  | INTEGER |

Enrollments Table
| Column        | Type    |
|---------------|---------|
| enrollment_id | INTEGER |
| student_id    | INTEGER |
| course_id     | INTEGER |
| grade         | TEXT    |

This schema was created using Python (`sqlite3`), and sample data is included.

Installation & Setup

1. Install Ollama (Windows)
Download from:
https://ollama.com/download/windows
After installation, open CMD and check:
ollama --version

2. Pull the Phi-3 Mini (3.8B) model
ollama pull phi3:mini

3. Run the Database Setup
python create_college_db.py
This generates `college.db`.



Example:
List all courses taken by John Doe
Example Output:
SELECT DISTINCT c.course_name
FROM Courses c
JOIN Enrollments e ON c.course_id = e.course_id
JOIN Students s ON s.student_id = e.student_id
WHERE s.name = 'John Doe';

DEMO YT LINK: https://youtu.be/9VThXzeD_Y4
