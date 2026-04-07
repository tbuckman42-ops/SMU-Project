from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.group_id_label.text = self.item["group_id"]
    self.student_id_label.text = self.item["student_id"]
    self.course_id_label.text = self.item["course_id"]
    self.group_name_label.text = self.item["group_name"]
    self.created_at_label.text = self.item["created_at"]
   

    # Any code you write here will run before the form opens.
