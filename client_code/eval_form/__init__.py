from ._anvil_designer import eval_formTemplate
from anvil import *


class eval_form(eval_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)