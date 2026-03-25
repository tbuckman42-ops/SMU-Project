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

    

    contribute_items = [("Contributes to Team Project", None), ("0- Never", 0), ("1- Sometimes", 1), ("2 Usually", 2), ("3- Regularly", 3), ("4- Always", 4)]
    facilitates_items = [("Facilitates Contributions of Others", None), ("0- Never", 0), ("1- Sometimes", 1), ("2 Usually", 2), ("3- Regularly", 3), ("4- Always", 4)]
    planning_items = [("Plans & Manages Team Project Goals", None), ("0- Never", 0), ("1- Sometimes", 1), ("2 Usually", 2), ("3- Regularly", 3), ("4- Always", 4)]
    fosters_items = [("Fosters a Team Climate", None), ("0- Never", 0), ("1- Sometimes", 1), ("2 Usually", 2), ("3- Regularly", 3), ("4- Always", 4)]
    manages_items = [("Manages Potential Conflict", None), ("0- Never", 0), ("1- Sometimes", 1), ("2 Usually", 2), ("3- Regularly", 3), ("4- Always", 4)]
    overall_items = [("Overall", None), ("0- Never", 0), ("1- Sometimes", 1), ("2 Usually", 2), ("3- Regularly", 3), ("4- Always", 4)]

    self.contribute_dd.items = contribute_items
    self.facilitates_dd.items = facilitates_items
    self.planning_dd.items = planning_items
    self.fosters_dd.items = fosters_items
    self.manages_dd.items = manages_items
    self.overall_dd.items = overall_items

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

  @handle("cancel_btn", "click")
  def cancel_btn_click(self, **event_args):
    dropdown = [
      self.contribute_dd,
      self.facilitates_dd,
      self.planning_dd,
      self.fosters_dd,
      self.manages_dd,
      self.overall_dd,
      self.student_dropdown
    ]

    for dd in dropdown:
        dd.selected_value = None
        
    
  pass

 


  
      