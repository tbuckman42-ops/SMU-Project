from ._anvil_designer import import_studentsTemplate
from anvil import *
import anvil.server
import csv
from io import StringIO
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class import_students(import_studentsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.csv_rows = []

    def student_uploader_change(self, file, **event_args):
      if not file:
        return

      if not file.name.lower().endswith(".csv"):
        alert("Please upload a CSV file.")
        return

      file_text = anvil.media.to_string(file)
      csv_reader = csv.DictReader(StringIO(file_text))

      required_columns = ["student_id", "first_name", "last_name", "email"]

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
          "student_id": row["student_id"].strip(),
          "first_name": row["first_name"].strip(),
          "last_name": row["last_name"].strip(),
          "email": row["email"].strip().lower()
        })

      self.csv_rows = rows
      self.repeating_panel_student.items = rows
 
  @handle("import_student_btn", "click")
  def import_student_btn_click(self, **event_args):
    if not self.csv_rows:
      alert("Please upload a CSV file first.")
      return

    try:
      result = anvil.server.call("import_students_from_grid", self.csv_rows)
      alert(result["message"])
    except Exception as e:
      alert(f"Import failed: {e}")


    # Any code you write here will run before the form opens.

  @handle("dashboard_btn", "click")
  def dashboard_btn_click(self, **event_args):
    open_form('professor_dashboard')
    pass
