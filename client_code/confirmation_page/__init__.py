from ._anvil_designer import confirmation_pageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class confirmation_page(confirmation_pageTemplate):
  def __init__(self, **properties):
    user = anvil.users.get_user()
    if not user or user['role'] not in ['student', 'admin']:
      alert("Access Denied")
      open_form('login')
      return
    self.init_components(**properties)

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

  @handle("home_btn_2", "click")
  def home_btn_2_click(self, **event_args):
    open_form('home_page')
