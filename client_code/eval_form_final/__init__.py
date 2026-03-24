from ._anvil_designer import eval_form_finalTemplate
from anvil import *
import anvil.server


class eval_form_final(eval_form_finalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.submit_btn.background = "#07123b"
    self.contribute_dd.width = "200px"
    self.manages_dd.width = "200px"
    self.fosters_dd.width = "200px"
    self.overall_dd.width = "200px"
    self.facilitates_dd.width = "200px"
    self.planning_dd.width = "200px"
    self.student_dropdown.width = "300px"

    

    rating_items = [
      ("Select a rating...", None),
      ("1. Poor", 1),
      ("2. Acceptable", 2),
      ("3. Good", 3),
      ("4. Excellent", 4)
    ]

    self.contribute_dd.items = rating_items
    self.facilitates_dd.items = rating_items
    self.planning_dd.items = rating_items
    self.fosters_dd.items = rating_items
    self.manages_dd.items = rating_items
    self.overall_dd.items = rating_items

    self.contribute_dd.selected_value = None
    self.facilitates_dd.selected_value = None
    self.planning_dd.selected_value = None
    self.fosters_dd.selected_value = None
    self.manages_dd.selected_value = None
    self.overall_dd.selected_value = None

   

    
   

  @handle("submit_btn", "click")
  def submit_btn_click(self, **event_args):
      if self.contribute_dd.selected_value is None:
        alert("Please complete Contributes to Team Project.")
        return

      if self.facilitates_dd.selected_value is None:
        alert("Please complete Facilitates Contributions of Others.")
        return

      if self.planning_dd.selected_value is None:
        alert("Please complete Planning and Management.")
        return

      if self.fosters_dd.selected_value is None:
        alert("Please complete Fosters a Team Climate.")
        return
    
      if self.manages_dd.selected_value is None:
        alert("Please complete Manages Potential Conflict.")
        return
    
      if self.overall_dd.selected_value is None:
        alert("Please complete Overall rating.")
        return
    
      alert("Evaluation submitted!")
  pass
      