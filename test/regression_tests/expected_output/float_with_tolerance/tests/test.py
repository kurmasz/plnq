
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

  
  @points(1)
  @name("test 1: final_value_monthly")
  def test_01(self):
      self.verify('final_value_monthly', answer.FloatAnswer(expected=15528.23,rel_tol=1e-09,abs_tol=0.01,strict=True), '[100, 10, 0.05]', -1, None)

  @points(1)
  @name("test 2: final_value_monthly")
  def test_02(self):
      self.verify('final_value_monthly', answer.FloatAnswer(expected=51905.73,rel_tol=1e-09,abs_tol=0.01,strict=True), '[150, 15, 0.08]', -1, None)

  @points(1)
  @name("test 3: final_value_monthly")
  def test_03(self):
      self.verify('final_value_monthly', answer.FloatAnswer(expected=13974.14,rel_tol=1e-09,abs_tol=0.01,strict=True), '[100, 10, 0.03]', -1, None)

  @points(1)
  @name("test 4: final_value_initial_plus_monthly")
  def test_04(self):
      self.verify('final_value_initial_plus_monthly', answer.FloatAnswer(expected=17175.239999999998,rel_tol=1e-09,abs_tol=0.01,strict=True), '[1000, 100, 10, 0.05]', -1, None)

  @points(1)
  @name("test 5: final_value_initial_plus_monthly")
  def test_05(self):
      self.verify('final_value_initial_plus_monthly', answer.FloatAnswer(expected=60173.04,rel_tol=1e-09,abs_tol=0.01,strict=True), '[2500, 150, 15, 0.08]', -1, None)

  @points(1)
  @name("test 6: final_value_initial_plus_monthly")
  def test_06(self):
      self.verify('final_value_initial_plus_monthly', answer.FloatAnswer(expected=2106978.48,rel_tol=1e-09,abs_tol=0.01,strict=True), '[10000, 500, 30, 0.12]', -1, None)

