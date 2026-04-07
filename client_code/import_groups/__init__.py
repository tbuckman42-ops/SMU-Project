from ._anvil_designer import import_groupsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
import csv
from io import StringIO

class import_groups(import_groupsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.csv_rows = []

  def groups_uploader_change(self, file, **event_args):
    if not file:
      return

    if not file.name.lower().endswith(".csv"):
      alert("Please upload a CSV file.")
      return

    file_text = anvil.media.to_string(file)
    csv_reader = csv.DictReader(StringIO(file_text))

    required_columns = ["group_id", "student_id", "course_id", "group_name", "created_at", "due_at"]

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
        "group_id": row["group_id"].strip(),
        "student_id": row["student_id"].strip(),
        "course_id": row["course_id"].strip(),
        "group_name": row["group_name"].strip(),
        "created_at": row["created_at"].strip(),
        "due_at": row["due_at"].strip()
      })

    self.csv_rows = rows
    self.repeating_panel_1.items = rows

  @handle("import_groups_btn", "click")
  def import_groups_btn_click(self, **event_args):
    if not self.csv_rows:
      alert("Please upload a CSV file first.")
      return

    try:
      result = anvil.server.call("import_groups_from_grid", self.csv_rows)
      alert(result["message"])
    except Exception as e:
      alert(f"Import failed: {e}")


  @handle("dashboard_btn", "click")
  def dashboard_btn_click(self, **event_args):
    open_form('professor_dashboard')
    pass
