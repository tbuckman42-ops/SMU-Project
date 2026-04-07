from ._anvil_designer import professor_dashboardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class professor_dashboard(professor_dashboardTemplate):
  def __init__(self, **properties):
    user = anvil.users.get_user()
    if not user or user['role'] not in ['professor', 'admin']:
      alert("Access Denied")
      open_form('login')
      return
    self.init_components(**properties)

  @handle("student_page", "click")
  def student_page_click(self, **event_args):
    open_form('import_students')

  @handle("course_page", "click")
  def course_page_click(self, **event_args):
    open_form('import_courses')

  @handle("group_page", "click")
  def group_page_click(self, **event_args):
    open_form('import_groups')

  @handle("home_btn", "click")
  def home_btn_click(self, **event_args):
    open_form('home_page')

  @handle("eval_btn", "click")
  def eval_btn_click(self, **event_args):
    open_form('eval_form_final')

  @handle("button_3", "click")
  def button_3_click(self, **event_args):
    open_form('tabular_search')

  @handle("chart_btn", "click")
  def chart_btn_click(self, **event_args):
    open_form('charts')

  @handle("dashboard_btn", "click")
  def dashboard_btn_click(self, **event_args):
    open_form('professor_dashboard')
  