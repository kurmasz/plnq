
from pl_helpers import name, points, not_repeated
from code_feedback import Feedback
from pl_unit_test import PLTestCaseWithPlot, PLTestCase
import json
import math

class Test(PLTestCaseWithPlot):
    
  def verify(self, function_name, expected, params_json):
    params = json.loads(params_json)
    observed = Feedback.call_user(getattr(self.st, function_name), *params)
    msg = f"'{function_name}({params_json})' did not return {expected} as expected. It returned {observed}."
   
    float_close = isinstance(expected, float) and math.isclose(expected, observed) 
    is_equal = (not isinstance(expected, float) and expected == observed)

    if (float_close or is_equal):
      Feedback.set_score(1)
    else:
      Feedback.add_feedback(msg)
      Feedback.set_score(0)

  student_code_file = 'learning_target.ipynb'

  # Make sure there is a newline here->

  