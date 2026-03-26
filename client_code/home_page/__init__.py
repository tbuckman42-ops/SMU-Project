from ._anvil_designer import home_pageTemplate
from anvil import *
import anvil.server


class home_page(home_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.group_name_dd.items = []
    self.student_name_dd.items = []
    self.load_courses()
    self.group_name_dd.set_event_handler("change", self.group_name_dd_change)
    self.course_id_dd.set_event_handler("change", self.course_id_dd_change)
    self.create_eval_btn.set_event_handler("click", self.create_eval_btn_click)

  def load_courses(self):
    self.course_id_dd.items = anvil.server.call("get_courses")
    

    
  def course_id_dd_change(self, **event_args):
    
    course_id = self.course_id_dd.selected_value
  
    if course_id is None:
      self.group_name_dd.items = []
      self.student_name_dd.items = []
      return
  
    self.group_name_dd.items = anvil.server.call(
      "get_groups_for_course",
      course_id
    )
    self.student_name_dd.items = []
  
  def group_name_dd_change(self, **event_args):
    
    group_name = self.group_name_dd.selected_value
    

    if group_name is None:
      self.student_name_dd.items = []
      return

    self.student_name_dd.items = anvil.server.call(
      "get_students_for_group_home",
      group_name
    )
    
    
  @handle("create_eval_btn", "click")
  def create_eval_btn_click(self, **event_args):
    
    course_id = self.course_id_dd.selected_value
    group_name = self.group_name_dd.selected_value
    evaluator_student_id = self.student_name_dd.selected_value
    due_at = self.due_date_picker.date

    if course_id is None or group_name is None or due_at is None:
      alert("Please select a course, group, and due date.")
      return

    try:
      result = anvil.server.call(
        "create_evaluation",
        course_id,
        group_name,
        due_at
      )

      anvil.open_form(
        "eval_form_final",
        evaluation_id=result["evaluation_id"],
        group_name=result["group_name"],
        evaluator_student_id=evaluator_student_id
        
      )

    except Exception as e:
      alert(f"Create evaluation failed: {e}")

  @handle("chart_btn", "click")
  def chart_btn_click(self, **event_args):
    open_form('charts')
    pass

  


  
  
  
