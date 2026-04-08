import pyodbc
import os
import anvil.server
import anvil.media
import requests
import csv
from io import StringIO
import random
from datetime import datetime

anvil.server.connect("server_OGC7RK4HCOVMD4R7F3TLKL44-YL4HR25YYQEGSUOY")

# Azure SQL Database connection parameters
server = 'peer-eval-server.database.windows.net'
database = 'peer-eval-db'
username = 'SeanLogin'
password = 'Peerevaldb#'
driver = 'ODBC Driver 18 for SQL Server'

# Connection string
connection_string = f'Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

conn = None

def get_connection():
    global conn
    try:
        if conn is None:
            conn = pyodbc.connect(connection_string)
        else:
            conn.cursor().execute("SELECT 1")
    except:
        conn = pyodbc.connect(connection_string)
    return conn

def make_evaluation_id():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        num = random.randint(0, 999)
        evaluation_id = f"E{num:03d}"

        cursor.execute("""
            SELECT 1
            FROM Evaluation
            WHERE evaluation_id = ?
        """, (evaluation_id,))

        if cursor.fetchone() is None:
            break

    cursor.close()
    return evaluation_id

def make_submission_id():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        num = random.randint(0, 999)
        submission_id = f"SUB{num:03d}"

        cursor.execute("""
            SELECT 1
            FROM Peer_Evaluation_Submission
            WHERE submission_id = ? 
        """, (submission_id))

        if cursor.fetchone() is None:
            break

    cursor.close()
    return submission_id

@anvil.server.callable
def get_courses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT course_id FROM Course")

    rows = cursor.fetchall()
    cursor.close()

    return [(row[0], row[0]) for row in rows]

@anvil.server.callable
def get_groups_for_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT group_name
        FROM Student_Group
        WHERE course_id = ?
        ORDER BY group_name
    """, (course_id,))

    rows = cursor.fetchall()
    cursor.close()

    return [(row[0], row[0]) for row in rows]

@anvil.server.callable
def get_students_for_group_home(group_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sg.student_id,
               s.first_name,
               s.last_name
        FROM Student_Group sg
        JOIN Student s
          ON s.student_id = sg.student_id
        WHERE sg.group_name = ?
        ORDER BY s.last_name, s.first_name
    """, (group_name,))

    rows = cursor.fetchall()
    cursor.close()

    return [(f"{row[1]} {row[2]}", row[0]) for row in rows]

@anvil.server.callable
def get_students_for_group(group_name, evaluator_student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sg.student_id, s.first_name, s.last_name
        FROM Student_Group sg
        JOIN Student s ON s.student_id = sg.student_id
        WHERE sg.group_name = ?
          AND sg.student_id <> ?
    """, (group_name, evaluator_student_id))

    rows = cursor.fetchall()
    cursor.close()

    return [(f"{row[1]} {row[2]}", row[0]) for row in rows]

@anvil.server.callable
def create_evaluation(course_id, group_name, due_at):
    conn = get_connection()
    cursor = conn.cursor()

    evaluation_id = make_evaluation_id()
    created_at = datetime.now()

    cursor.execute("""
        INSERT INTO Evaluation (
            evaluation_id,
            course_id,
            group_name,
            created_at,
            due_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        evaluation_id,
        course_id,
        group_name,
        created_at,
        due_at
    ))
    conn.commit()
    cursor.close()

    return {
        "group_name": group_name,
        "evaluation_id": evaluation_id
    }

@anvil.server.callable
def save_evaluation_score(
    evaluation_id,
    evaluator_student_id,
    evaluated_student_id,
    contributes_score,
    facilitates_score,
    planning_mgmt_score,
    team_climate_score,
    conflict_mgmt_score,
    overall_score
):
    if evaluator_student_id == evaluated_student_id:
        raise ValueError("A student cannot evaluate themself.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM Evaluation
        WHERE evaluation_id = ?
    """, (evaluation_id,))
    if cursor.fetchone() is None:
        cursor.close()
        raise ValueError("Invalid evaluation_id.")

    cursor.execute("SELECT 1 FROM Student WHERE student_id = ?", (evaluator_student_id,))
    if cursor.fetchone() is None:
        cursor.close()
        raise ValueError("Invalid evaluator_student_id.")

    cursor.execute("SELECT 1 FROM Student WHERE student_id = ?", (evaluated_student_id,))
    if cursor.fetchone() is None:
        cursor.close()
        raise ValueError("Invalid evaluated_student_id.")

    cursor.execute("""
        SELECT 1
        FROM Peer_Evaluation_Submission
        WHERE evaluation_id = ?
          AND evaluator_student_id = ?
          AND evaluated_student_id = ?
    """, (evaluation_id, evaluator_student_id, evaluated_student_id))

    if cursor.fetchone() is not None:
        cursor.close()
        raise ValueError("This evaluation has already been submitted for that student.")

    submission_id = make_submission_id()
    submission_time = datetime.now()

    cursor.execute("""
        INSERT INTO Peer_Evaluation_Submission (
            submission_id,
            evaluation_id,
            evaluator_student_id,
            evaluated_student_id,
            submission_time
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        submission_id,
        evaluation_id,
        evaluator_student_id,
        evaluated_student_id,
        submission_time
    ))

    cursor.execute("""
        INSERT INTO Evaluation_Score (
            submission_id,
            evaluation_id,
            contributes_score,
            facilitates_score,
            planning_mgmt_score,
            team_climate_score,
            conflict_mgmt_score,
            overall_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        submission_id,
        evaluation_id,
        contributes_score,
        facilitates_score,
        planning_mgmt_score,
        team_climate_score,
        conflict_mgmt_score,
        overall_score
    ))
    conn.commit()
    cursor.close()

    return {
        "message": "Evaluation submitted successfully.",
        "submission_id": submission_id
    }

@anvil.server.callable
def send_to_zoho(payload):
    response = requests.post(
        "https://flow.zoho.com/918462572/flow/webhook/incoming?zapikey=1001.4a6ad7a3bfa989e0b5364ef37d8fa628.a7115ab81166d5d4b7320b60263628fb&isdebug=false",
        json=payload,
        headers={"Content-Type": "application/json"})
    
    response.raise_for_status()
    return {"text": response.text, "status_code": response.status_code}

def parse_datetime(dt_string):
    dt_string = dt_string.strip()
    return datetime.fromisoformat(dt_string)

@anvil.server.callable
def parse_students_csv(file):
    file_text = file.get_bytes().decode("utf-8-sig")
    csv_reader = csv.DictReader(StringIO(file_text))

    required_columns = ["student_id", "first_name", "last_name", "email"]

    if not csv_reader.fieldnames:
        raise Exception("The CSV file is empty or invalid.")

    missing = [col for col in required_columns if col not in csv_reader.fieldnames]
    if missing:
        raise Exception("Missing required columns: " + ", ".join(missing))

    rows = []
    for row in csv_reader:
        rows.append({
            "student_id": row["student_id"].strip(),
            "first_name": row["first_name"].strip(),
            "last_name": row["last_name"].strip(),
            "email": row["email"].strip().lower()
        })

    return rows

@anvil.server.callable
def import_students_from_grid(rows):
    conn = get_connection()
    cursor = conn.cursor()

    inserted_rows = 0
    skipped_rows = 0

    try:
        for row in rows:
            student_id = row["student_id"].strip()
            first_name = row["first_name"].strip()
            last_name = row["last_name"].strip()
            email = row["email"].strip().lower()

            cursor.execute("""
                SELECT student_id
                FROM STUDENT
                WHERE student_id = ?
            """, (student_id,))
            existing_student = cursor.fetchone()

            if existing_student:
                skipped_rows += 1
                continue

            cursor.execute("""
                INSERT INTO STUDENT (student_id, first_name, last_name, email)
                VALUES (?, ?, ?, ?)
            """, (student_id, first_name, last_name, email))

            inserted_rows += 1

        conn.commit()

        return {
            "message": f"Import complete. {inserted_rows} students inserted, {skipped_rows} skipped."
        }

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

@anvil.server.callable
def parse_courses_csv(file):
    file_text = file.get_bytes().decode("utf-8-sig")
    csv_reader = csv.DictReader(StringIO(file_text))

    required_columns = ["course_id", "course_name", "professor_id"]

    if not csv_reader.fieldnames:
        raise Exception("The CSV file is empty or invalid.")

    missing = [col for col in required_columns if col not in csv_reader.fieldnames]
    if missing:
        raise Exception("Missing required columns: " + ", ".join(missing))

    rows = []
    for row in csv_reader:
        rows.append({
            "course_id": row["course_id"].strip(),
            "course_name": row["course_name"].strip(),
            "professor_id": row["professor_id"].strip()
        })

    return rows

@anvil.server.callable
def import_courses_from_grid(rows):
    conn = get_connection()
    cursor = conn.cursor()

    inserted_rows = 0
    skipped_rows = 0

    try:
        for row in rows:
            course_id = row["course_id"].strip()
            course_name = row["course_name"].strip()
            professor_id = row["professor_id"].strip()

            cursor.execute("""
                SELECT course_id
                FROM COURSE
                WHERE course_id = ?
            """, (course_id,))
            existing_course = cursor.fetchone()

            if existing_course:
                skipped_rows += 1
                continue

            cursor.execute("""
                SELECT professor_id
                FROM PROFESSOR
                WHERE professor_id = ?
            """, (professor_id,))
            existing_professor = cursor.fetchone()

            if not existing_professor:
                skipped_rows += 1
                continue

            cursor.execute("""
                INSERT INTO COURSE (course_id, course_name, professor_id)
                VALUES (?, ?, ?)
            """, (course_id, course_name, professor_id))

            inserted_rows += 1

        conn.commit()

        return {
            "message": f"Import complete. {inserted_rows} courses inserted, {skipped_rows} skipped."
        }

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

@anvil.server.callable
def parse_groups_csv(file):
    file_text = file.get_bytes().decode("utf-8-sig")
    csv_reader = csv.DictReader(StringIO(file_text))

    required_columns = ["group_id", "course_id", "student_id", "group_name", "created_at"]

    if not csv_reader.fieldnames:
        raise Exception("The CSV file is empty or invalid.")

    missing = [col for col in required_columns if col not in csv_reader.fieldnames]
    if missing:
        raise Exception("Missing required columns: " + ", ".join(missing))

    rows = []
    for row in csv_reader:
        rows.append({
            "group_id": row["group_id"].strip(),
            "course_id": row["course_id"].strip(),
            "student_id": row["student_id"].strip(),
            "group_name": row["group_name"].strip(),
            "created_at": row["created_at"].strip()
        })

    return rows

@anvil.server.callable
def import_groups_from_grid(rows):
    conn = get_connection()
    cursor = conn.cursor()

    inserted_rows = 0
    skipped_rows = 0

    try:
        for row in rows:
            group_id = row["group_id"].strip()
            course_id = row["course_id"].strip()
            student_id = row["student_id"].strip()
            group_name = row["group_name"].strip()
            created_at = parse_datetime(row["created_at"])

            cursor.execute("""
                SELECT course_id
                FROM COURSE
                WHERE course_id = ?
            """, (course_id,))
            existing_course = cursor.fetchone()

            if not existing_course:
                skipped_rows += 1
                continue

            cursor.execute("""
                SELECT student_id
                FROM STUDENT
                WHERE student_id = ?
            """, (student_id,))
            existing_student = cursor.fetchone()

            if not existing_student:
                skipped_rows += 1
                continue

            cursor.execute("""
                SELECT group_id
                FROM STUDENT_GROUP
                WHERE group_id = ?
            """, (group_id,))
            existing_group = cursor.fetchone()

            if existing_group:
                skipped_rows += 1
                continue

            cursor.execute("""
                INSERT INTO STUDENT_GROUP (group_id, course_id, student_id, group_name, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (group_id, course_id, student_id, group_name, created_at))

            inserted_rows += 1

        conn.commit()

        return {
            "message": f"Import complete. {inserted_rows} groups inserted, {skipped_rows} skipped."
        }

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

@anvil.server.callable
def test_uplink():
    return "Uplink is working!"

anvil.server.wait_forever()
