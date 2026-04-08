import pyodbc
import os
import anvil.server
import requests
import random
from datetime import datetime
anvil.server.connect("server_OGC7RK4HCOVMD4R7F3TLKL44-YL4HR25YYQEGSUOY")
# Azure SQL Database connection parameters
server = 'peer-eval-server.database.windows.net'
database = 'peer-eval-db'
username = 'SeanLogin'
password = 'Peerevaldb#'
driver =  "/opt/homebrew/lib/libmsodbcsql.18.dylib" #'{ODBC Driver 18 for SQL Server}'

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
        SELECT gm.student_id,
               s.first_name,
               s.last_name
        FROM Student_Group sg
        JOIN Group_Member gm
          ON gm.group_id = sg.group_id
        JOIN Student s
          ON s.student_id = gm.student_id
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
        SELECT gm.student_id, s.first_name, s.last_name
        FROM Student_Group sg
        JOIN Group_Member gm ON gm.group_id = sg.group_id
        JOIN Student s ON s.student_id = gm.student_id
        WHERE sg.group_name = ?
          AND gm.student_id <> ?
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

    # check evaluation exists
    cursor.execute("""
        SELECT 1
        FROM Evaluation
        WHERE evaluation_id = ?
    """, (evaluation_id,))
    if cursor.fetchone() is None:
        cursor.close()
        raise ValueError("Invalid evaluation_id.")
    # check both students exist
    cursor.execute("SELECT 1 FROM Student WHERE student_id = ?", (evaluator_student_id,))
    if cursor.fetchone() is None:
        cursor.close()
        raise ValueError("Invalid evaluator_student_id.")
    cursor.execute("SELECT 1 FROM Student WHERE student_id = ?", (evaluated_student_id,))
    if cursor.fetchone() is None:
        cursor.close()
        raise ValueError("Invalid evaluated_student_id.")
    #to stop duplicates
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
    return {"text": response.text, "status_code":response.status_code}



@anvil.server.callable
def test_uplink():
    return "Uplink is working!"
# --- connect to Anvil (ALWAYS at bottom) ---

anvil.server.wait_forever()


    

        
