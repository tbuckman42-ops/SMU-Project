from ._anvil_designer import confirmation_pageTemplate
from anvil import *
import anvil.server


class confirmation_page(confirmation_pageTemplate):
  def __init__(self, **properties):
    
    self.init_components(**properties)
    
   

    
    
    # Any code you write here will run before the form opens.

  @handle("home_btn", "click")
  def home_btn_click(self, **event_args):
    open_form('home_page')
    pass

  @handle("chart_btn", "click")
  def chart_btn_click(self, **event_args):
    open_form('charts')
    pass

  @handle("home_btn_2", "click")
  def home_btn_2_click(self, **event_args):
    open_form('home_page')
    pass
