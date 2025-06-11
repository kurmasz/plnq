
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
  @name("test 1: extract_phone")
  def test_01(self):
      self.verify('extract_phone', '6162314455', '["616-231-4455"]', -1, None)

  @points(1)
  @name("test 2: extract_phone")
  def test_02(self):
      self.verify('extract_phone', None, '["(616)-231-4455"]', -1, None)

  @points(1)
  @name("test 3: extract_phone")
  def test_03(self):
      self.verify('extract_phone', None, '["616-231-445"]', -1, None)

  @points(1)
  @name("test 4: extract_phone")
  def test_04(self):
      self.verify('extract_phone', '5174328841', '["517-432-8841"]', -1, None)

  @points(1)
  @name("test 5: extract_phone")
  def test_05(self):
      self.verify('extract_phone', '3137352132', '["313-735-2132"]', -1, None)

  @points(1)
  @name("test 6: extract_phone")
  def test_06(self):
      self.verify('extract_phone', None, '["1-313-735-2132"]', -1, None)

  @points(1)
  @name("test 7: extract_phone")
  def test_07(self):
      self.verify('extract_phone', None, '["313-75-2132"]', -1, None)

  @points(1)
  @name("test 8: parse_format")
  def test_08(self):
      self.verify('parse_format', ('D', '-', 'g'), '["D-g"]', -1, None)

  @points(1)
  @name("test 9: parse_format")
  def test_09(self):
      self.verify('parse_format', (None, None, 'k'), '["k"]', -1, None)

  @points(1)
  @name("test 10: parse_format")
  def test_10(self):
      self.verify('parse_format', (None, ':', 'y'), '[":y"]', -1, None)

  @points(1)
  @name("test 11: parse_format")
  def test_11(self):
      self.verify('parse_format', ('>', '--', 'm'), '[">--m"]', -1, None)

  @points(1)
  @name("test 12: parse_format")
  def test_12(self):
      self.verify('parse_format', None, '["Dm--z"]', -1, None)

  @points(1)
  @name("test 13: parse_format")
  def test_13(self):
      self.verify('parse_format', ('X', '-.', 'w'), '["X-.w"]', -1, None)

  @points(1)
  @name("test 14: parse_format")
  def test_14(self):
      self.verify('parse_format', ('X', '-.', None), '["X-."]', -1, None)

  @points(1)
  @name("test 15: parse_format")
  def test_15(self):
      self.verify('parse_format', (None, '-.', 'w'), '["-.w"]', -1, None)

  @points(1)
  @name("test 16: parse_format")
  def test_16(self):
      self.verify('parse_format', (None, '-.', None), '["-."]', -1, None)

  @points(1)
  @name("test 17: parse_format")
  def test_17(self):
      self.verify('parse_format', ('X', None, 'w'), '["Xw"]', -1, None)

  @points(1)
  @name("test 18: parse_format")
  def test_18(self):
      self.verify('parse_format', ('X', None, None), '["X"]', -1, None)

  @points(1)
  @name("test 19: parse_format")
  def test_19(self):
      self.verify('parse_format', (None, None, 'w'), '["w"]', -1, None)

  @points(1)
  @name("test 20: parse_format")
  def test_20(self):
      self.verify('parse_format', ('d', ':', 'c'), '["d:c"]', -1, None)

  @points(1)
  @name("test 21: get_first_quote")
  def test_21(self):
      self.verify('get_first_quote', 'Pickles', '["Here comes \\"Pickles\\" and \\"Wheezer\\"."]', -1, None)

  @points(1)
  @name("test 22: get_first_quote")
  def test_22(self):
      self.verify('get_first_quote', None, '["There are no quotes here"]', -1, None)

  @points(1)
  @name("test 23: get_first_quote")
  def test_23(self):
      self.verify('get_first_quote', 'Stretch', '["More nicknames: \\"Stretch\\", \\"Gravity\\", \\"Rainmaker\\""]', -1, None)

  @points(1)
  @name("test 24: get_first_quote")
  def test_24(self):
      self.verify('get_first_quote', None, '["This is a \\"Partial quotation"]', -1, None)

  @points(1)
  @name("test 25: get_first_quote")
  def test_25(self):
      self.verify('get_first_quote', 'quote', '["End with a \\"quote\\""]', -1, None)

