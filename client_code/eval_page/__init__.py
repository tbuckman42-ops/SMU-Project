from ._anvil_designer import eval_pageTemplate
from anvil import *

class eval_page(eval_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
