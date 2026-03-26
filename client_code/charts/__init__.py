from ._anvil_designer import chartsTemplate
from anvil import *
import anvil.server


class charts(chartsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("home_btn", "click")
  def home_btn_click(self, **event_args):
    open_form('home_page')
    pass
