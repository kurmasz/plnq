
from pl_helpers import name, points, not_repeated
from code_feedback import Feedback
from pl_unit_test import PLTestCaseWithPlot, PLTestCase
import json
import math

import answer

class Test(PLTestCaseWithPlot):
    
  def verify(self, function_name, expected, params_json):
    params = json.loads(params_json)
    observed = Feedback.call_user(getattr(self.st, function_name), *params)
    # msg = f"'{function_name}({params_json})' did not return {expected} as expected. It returned {observed}."
   
    verifier = answer.Answer.make(expected)

    # float_close = isinstance(expected, float) and math.isclose(expected, observed) 
    # is_equal = (not isinstance(expected, float) and expected == observed)

    if (verifier.verify(observed)):
      Feedback.set_score(1)
    else:
      Feedback.add_feedback(f"'{function_name}({params_json})': {verifier.message()}")
      Feedback.set_score(0)

  student_code_file = 'learning_target.ipynb'

  # Make sure there is a newline here->

  