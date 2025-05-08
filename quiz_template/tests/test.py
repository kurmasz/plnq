
from pl_helpers import name, points, not_repeated
from code_feedback import Feedback
from pl_unit_test import PLTestCaseWithPlot, PLTestCase
import json

# These imports are needed because the test generation code from the template may use them.
# (TODO: Is there a way to get the template to provide any necessary import statements?)
import math
import re

import answer

class Test(PLTestCaseWithPlot):
    
  def verify(self, function_name, expected, params_json, param_index=-1, cast=None):
    original_params = json.loads(params_json)
    params = json.loads(params_json)
    return_value = Feedback.call_user(getattr(self.st, function_name), *params)
    if cast and cast != type(None):
      return_value = cast(return_value)

    verifier = answer.Answer.make(expected)

    if (param_index == -1):
      observed = return_value
    else:
      observed = params[param_index]

    if (verifier.verify(observed)):
      Feedback.set_score(1)
    else:
      Feedback.add_feedback(f"'{function_name}({params_json})': {verifier.message()}")
      Feedback.set_score(0)



  student_code_file = 'learning_target.ipynb'

  # Make sure there is a newline here->

  