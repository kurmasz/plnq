
from pl_helpers import name, points
from code_feedback import Feedback
from pl_unit_test import PLTestCase
import json

# These imports are needed because the test generation code from the template may use them.
# (TODO: Is there a way to get the template to provide any necessary import statements?)
import math
import re

import answer

class Test(PLTestCase):
    
  def verify(self, function_name, expected, params_json, param_index=-1, cast=None):
    # original_params = json.loads(params_json)
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

  
  @points(1)
  @name("test 1: letters_in_string")
  def test_01(self):
      self.verify('letters_in_string', 10, '["Hello, World!"]', -1, None)

  @points(1)
  @name("test 2: letters_in_string")
  def test_02(self):
      self.verify('letters_in_string', 30, '["To be, or not to be: that is the question."]', -1, None)

  @points(1)
  @name("test 3: letters_in_string")
  def test_03(self):
      self.verify('letters_in_string', 3, '["C-3PO"]', -1, None)

  @points(1)
  @name("test 4: letters_in_string")
  def test_04(self):
      self.verify('letters_in_string', 2, '["R2D2"]', -1, None)

  @points(1)
  @name("test 5: letters_in_string")
  def test_05(self):
      self.verify('letters_in_string', 25, '["Fourscore and seven years ago"]', -1, None)

  @points(1)
  @name("test 6: letters_in_string")
  def test_06(self):
      self.verify('letters_in_string', 0, '[""]', -1, None)

  @points(1)
  @name("test 7: letters_in_string")
  def test_07(self):
      self.verify('letters_in_string', 3, '["Mom"]', -1, None)

  @points(1)
  @name("test 8: letters_in_string")
  def test_08(self):
      self.verify('letters_in_string', 0, '["12345"]', -1, None)

  @points(1)
  @name("test 9: letters_in_string")
  def test_09(self):
      self.verify('letters_in_string', 0, '["1 2 3 4 5"]', -1, None)

  @points(1)
  @name("test 10: num_long_words")
  def test_10(self):
      self.verify('num_long_words', 2, '["Ivan the Terrible", 4]', -1, None)

  @points(1)
  @name("test 11: num_long_words")
  def test_11(self):
      self.verify('num_long_words', 3, '["Imagination is more important than knowledge.", 5]', -1, None)

  @points(1)
  @name("test 12: num_long_words")
  def test_12(self):
      self.verify('num_long_words', 1, '["Ivan the Terrible", 5]', -1, None)

  @points(1)
  @name("test 13: num_long_words")
  def test_13(self):
      self.verify('num_long_words', 0, '["Ivan the Terrible", 9]', -1, None)

  @points(1)
  @name("test 14: num_long_words")
  def test_14(self):
      self.verify('num_long_words', 3, '["Ivan the Terrible", 3]', -1, None)

  @points(1)
  @name("test 15: num_long_words")
  def test_15(self):
      self.verify('num_long_words', 3, '["Imagination is more important than knowledge", 5]', -1, None)

  @points(1)
  @name("test 16: num_long_words")
  def test_16(self):
      self.verify('num_long_words', 1, '["Imagination is more important than knowledge", 10]', -1, None)

  @points(1)
  @name("test 17: num_long_words")
  def test_17(self):
      self.verify('num_long_words', 0, '["Imagination is more important than knowledge", 12]', -1, None)

  @points(1)
  @name("test 18: num_long_words")
  def test_18(self):
      self.verify('num_long_words', 3, '["Imagination is more important than knowledge", 9]', -1, None)

  @points(1)
  @name("test 19: num_long_words")
  def test_19(self):
      self.verify('num_long_words', 5, '["Imagination is more important than knowledge", 3]', -1, None)

  @points(1)
  @name("test 20: first_alphabetically")
  def test_20(self):
      self.verify('first_alphabetically', 'ivan', '["Ivan the Terrible"]', -1, None)

  @points(1)
  @name("test 21: first_alphabetically")
  def test_21(self):
      self.verify('first_alphabetically', 'lose', '["You win some, you lose some"]', -1, None)

  @points(1)
  @name("test 22: first_alphabetically")
  def test_22(self):
      self.verify('first_alphabetically', 'but', '["Life is really simple, but we insist on making it complicated"]', -1, None)

  @points(1)
  @name("test 23: first_alphabetically")
  def test_23(self):
      self.verify('first_alphabetically', 'a', '["Life is like a box of chocolates"]', -1, None)

  @points(1)
  @name("test 24: create_abbreviation")
  def test_24(self):
      self.verify('create_abbreviation', 'USA', '["United States of America"]', -1, None)

  @points(1)
  @name("test 25: create_abbreviation")
  def test_25(self):
      self.verify('create_abbreviation', 'IUCN', '["International Union for the Conservation of Nature"]', -1, None)

  @points(1)
  @name("test 26: create_abbreviation")
  def test_26(self):
      self.verify('create_abbreviation', 'CIA', '["Central Intelligence Agency"]', -1, None)

  @points(1)
  @name("test 27: create_abbreviation")
  def test_27(self):
      self.verify('create_abbreviation', 'FBI', '["Federal Bureau of Investigation"]', -1, None)

  @points(1)
  @name("test 28: create_abbreviation")
  def test_28(self):
      self.verify('create_abbreviation', 'UAL', '["University of the Arts London"]', -1, None)

  @points(1)
  @name("test 29: create_abbreviation")
  def test_29(self):
      self.verify('create_abbreviation', 'CSPC', '["Center for the Study of the Presidency and Congress"]', -1, None)

