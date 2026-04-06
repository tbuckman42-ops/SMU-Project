from ._anvil_designer import professor_dashboardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class professor_dashboard(professor_dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("student_page", "click")
  def student_page_click(self, **event_args):
    open_form('import_students')
    pass

  @handle("course_page", "click")
  def course_page_click(self, **event_args):
    open_form('import_courses')
    pass

  @handle("group_page", "click")
  def group_page_click(self, **event_args):
    open_form('import_groups')
    pass
