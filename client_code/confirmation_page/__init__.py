from ._anvil_designer import confirmation_pageTemplate
from anvil import *
import anvil.server


class confirmation_page(confirmation_pageTemplate):
  def __init__(self, **properties):
    
    self.init_components(**properties)
    self.name_area.width = "100px"
    
    
    # Any code you write here will run before the form opens.
