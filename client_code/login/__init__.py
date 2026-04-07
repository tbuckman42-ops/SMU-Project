from ._anvil_designer import loginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class login(loginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    # Any code you write here will run before the form opens.

  @handle("login_btn", "click")
  def login_button_click(self, **event_args):
    user = anvil.users.login_with_email(
      self.user_email.text,
      self.password.text
    )
    if user:
      role = user['role']
      if role == 'professor':
        open_form('professor_dashboard')
      elif role == 'student':
        open_form('home_page')
      elif role == 'admin':
        open_form('professor_dashboard')
      else:
        alert("No role assigned. Contact administrator.")
    else:
      alert("Invalid email or password.")

