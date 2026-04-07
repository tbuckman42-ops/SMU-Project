from ._anvil_designer import import_coursesTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
import csv
from io import StringIO

class import_courses(import_coursesTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.csv_rows = []

  def courses_uploader_change(self, file, **event_args):
    if not file:
      return

    if not file.name.lower().endswith(".csv"):
      alert("Please upload a CSV file.")
      return

    file_text = anvil.media.to_string(file)
    csv_reader = csv.DictReader(StringIO(file_text))

    required_columns = ["course_id", "course_name", "professor_name"]

    if not csv_reader.fieldnames:
      alert("The CSV file is empty or invalid.")
      return

    missing = [col for col in required_columns if col not in csv_reader.fieldnames]
    if missing:
      alert("Missing required columns: " + ", ".join(missing))
      return

    rows = []
    for row in csv_reader:
      rows.append({
        "course_id": row["course_id"].strip(),
        "course_name": row["course_name"].strip(),
        "professor_name": row["professor_name"].strip()
      })

    self.csv_rows = rows
    self.course_panel.items = rows

  @handle("import_courses_btn", "click")
  def import_courses_btn_click(self, **event_args):
    if not self.csv_rows:
      alert("Please upload a CSV file first.")
      return

    try:
      result = anvil.server.call("import_courses_from_grid", self.csv_rows)
      alert(result["message"])
    except Exception as e:
      alert(f"Import failed: {e}")
    # Any code you write here will run before the form opens.

  @handle("dashboard_btn", "click")
  def dashboard_btn_click(self, **event_args):
    open_form('professor_dashboard')
    pass

  
