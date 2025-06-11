
from pl_helpers import name, points
from code_feedback import Feedback
from pl_unit_test import PLTestCase
import json

# These imports are needed because the test generation code from the template may use them.
# (TODO: Is there a way to get the template to provide any necessary import statements?)
import math
import re
import sys

import answer

class Test(PLTestCase):
    
  def verify(self, function_name, expected, params_json, param_index=-1, cast=None):
    # original_params = json.loads(params_json)
    params = json.loads(params_json)

    # Remove the opening and closing brackets if they exist.
    # (They should exist, because params should be a JSON array.
    # TODO: It would be nice to have a space after the commas; but
    # trying to add that would open a rather large can of worms, 
    # because we would need to figure out which commas are from the 
    # list, and which would be in literal strings. And there are 
    # other cases I probably haven't thought of.)
    if params_json.startswith('[') and params_json.endswith(']'):
      params_to_print = params_json[1:-1]
    else:
      print("Warning: params_json does not start and end with brackets.", sys.stderr, flush=True)
      params_to_print = params_json

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
      Feedback.add_feedback(f"{function_name}({params_to_print}): {verifier.message()}")
      Feedback.set_score(0)



  student_code_file = 'learning_target.ipynb'

  # Make sure there is a newline here->

  