
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
  @name("test 1: largest_population")
  def test_01(self):
      self.verify('largest_population', 'California', '["states.txt"]', -1, None)

  @points(1)
  @name("test 2: largest_population")
  def test_02(self):
      self.verify('largest_population', 'Ontario', '["canada.txt"]', -1, None)

  @points(1)
  @name("test 3: largest_population")
  def test_03(self):
      self.verify('largest_population', 'London', '["europe_capitals.txt"]', -1, None)

  @points(1)
  @name("test 4: first_match")
  def test_04(self):
      self.verify('first_match', 'Georgia: 10711908', '["states.txt", "Georgia"]', -1, None)

  @points(1)
  @name("test 5: first_match")
  def test_05(self):
      self.verify('first_match', 'North Carolina: 10852983', '["states.txt", "North"]', -1, None)

  @points(1)
  @name("test 6: first_match")
  def test_06(self):
      self.verify('first_match', 'New Hampshire: 1402538', '["states.txt", "New"]', -1, None)

  @points(1)
  @name("test 7: first_match")
  def test_07(self):
      self.verify('first_match', 'Kentucky: 4512310', '["states.txt", "y"]', -1, None)

  @points(1)
  @name("test 8: first_match")
  def test_08(self):
      self.verify('first_match', 'New Brunswick: 804469', '["canada.txt", "New"]', -1, None)

  @points(1)
  @name("test 9: first_match")
  def test_09(self):
      self.verify('first_match', 'Ljubljana: 295504', '["europe_capitals.txt", "j"]', -1, None)

  @points(1)
  @name("test 10: last_match")
  def test_10(self):
      self.verify('last_match', 'Georgia: 10711908', '["states.txt", "Georgia"]', -1, None)

  @points(1)
  @name("test 11: last_match")
  def test_11(self):
      self.verify('last_match', 'North Dakota: 779261', '["states.txt", "North"]', -1, None)

  @points(1)
  @name("test 12: last_match")
  def test_12(self):
      self.verify('last_match', 'New York: 19677151', '["states.txt", "New"]', -1, None)

  @points(1)
  @name("test 13: last_match")
  def test_13(self):
      self.verify('last_match', 'Wyoming: 581381', '["states.txt", "y"]', -1, None)

  @points(1)
  @name("test 14: last_match")
  def test_14(self):
      self.verify('last_match', 'Newfoundland and Labrador: 522994', '["canada.txt", "New"]', -1, None)

  @points(1)
  @name("test 15: last_match")
  def test_15(self):
      self.verify('last_match', 'Sarajevo: 275524', '["europe_capitals.txt", "j"]', -1, None)

