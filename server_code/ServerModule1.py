import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import csv
from io import StringIO
import anvil.media

@anvil.server.callable
def parse_students_csv(file):
  file_text = anvil.media.to_string(file)
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
  def parse_courses_csv(file):
    file_text = anvil.media.to_string(file)
    csv_reader = csv.DictReader(StringIO(file_text))
    required_columns = ["course_id", "course_name", "professor_name"]
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
        "professor_name": row["professor_name"].strip()
      })
    return rows
  @anvil.server.callable
  def parse_groups_csv(file):
    file_text = anvil.media.to_string(file)
    csv_reader = csv.DictReader(StringIO(file_text))
    required_columns = ["group_id", "student_id", "course_id", "group_name", "created_at", "due_at"]
    if not csv_reader.fieldnames:
      raise Exception("The CSV file is empty or invalid.")
    missing = [col for col in required_columns if col not in csv_reader.fieldnames]
    if missing:
      raise Exception("Missing required columns: " + ", ".join(missing))
    rows = []
    for row in csv_reader:
      rows.append({
        "group_id": row["group_id"].strip(),
        "student_id": row["student_id"].strip(),
        "course_id": row["course_id"].strip(),
        "group_name": row["group_name"].strip(),
        "created_at": row["created_at"].strip(),
        "due_at": row["due_at"].strip()
      })
    return rows
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
