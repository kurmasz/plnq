
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

  
  @points(1)
  @name("test 1: remove_suffixes")
  def test_01(self):
      self.verify('remove_suffixes', answer.InlineAnswer(expected=['A', 'A', 'C', 'D'],expected_return_value=None,param_index=0), '[["A", "A-", "C+", "D"]]', 0, None)

  @points(1)
  @name("test 2: remove_suffixes")
  def test_02(self):
      self.verify('remove_suffixes', answer.InlineAnswer(expected=['B'],expected_return_value=None,param_index=0), '[["B+"]]', 0, None)

  @points(1)
  @name("test 3: remove_suffixes")
  def test_03(self):
      self.verify('remove_suffixes', answer.InlineAnswer(expected=['C'],expected_return_value=None,param_index=0), '[["C"]]', 0, None)

  @points(1)
  @name("test 4: remove_suffixes")
  def test_04(self):
      self.verify('remove_suffixes', answer.InlineAnswer(expected=[],expected_return_value=None,param_index=0), '[[]]', 0, None)

  @points(1)
  @name("test 5: truncate")
  def test_05(self):
      self.verify('truncate', answer.InlineAnswer(expected=[1, 2, 0, 4, 5, 10, 10],expected_return_value=None,param_index=2), '[0, 10, [1, 2, -3, 4, 5, 11, 12]]', 2, None)

  @points(1)
  @name("test 6: truncate")
  def test_06(self):
      self.verify('truncate', answer.InlineAnswer(expected=[3, 3, 4, 5, 6, 7, 7],expected_return_value=None,param_index=2), '[3, 7, [2, 3, 4, 5, 6, 7, 8]]', 2, None)

  @points(1)
  @name("test 7: truncate")
  def test_07(self):
      self.verify('truncate', answer.InlineAnswer(expected=[6, 6, 6, 6],expected_return_value=None,param_index=2), '[6, 8, [1, 2, 0, 3]]', 2, None)

  @points(1)
  @name("test 8: truncate")
  def test_08(self):
      self.verify('truncate', answer.InlineAnswer(expected=[8, 8, 8, 8],expected_return_value=None,param_index=2), '[6, 8, [11, 12, 10, 13]]', 2, None)

  @points(1)
  @name("test 9: truncate")
  def test_09(self):
      self.verify('truncate', answer.InlineAnswer(expected=[6, 7, 6, 7],expected_return_value=None,param_index=2), '[5, 8, [6, 7, 6, 7]]', 2, None)

  @points(1)
  @name("test 10: truncate")
  def test_10(self):
      self.verify('truncate', answer.InlineAnswer(expected=[],expected_return_value=None,param_index=2), '[5, 8, []]', 2, None)

  @points(1)
  @name("test 11: truncate_and_count")
  def test_11(self):
      self.verify('truncate_and_count', answer.InlineAnswer(expected=[1, 2, 0, 4, 5, 10, 10],expected_return_value=3,param_index=2), '[0, 10, [1, 2, -3, 4, 5, 11, 12]]', 2, None)

  @points(1)
  @name("test 12: truncate_and_count")
  def test_12(self):
      self.verify('truncate_and_count', answer.InlineAnswer(expected=[3, 3, 4, 5, 6, 7, 7],expected_return_value=2,param_index=2), '[3, 7, [2, 3, 4, 5, 6, 7, 8]]', 2, None)

  @points(1)
  @name("test 13: truncate_and_count")
  def test_13(self):
      self.verify('truncate_and_count', answer.InlineAnswer(expected=[6, 6, 6, 6],expected_return_value=4,param_index=2), '[6, 8, [1, 2, 0, 3]]', 2, None)

  @points(1)
  @name("test 14: truncate_and_count")
  def test_14(self):
      self.verify('truncate_and_count', answer.InlineAnswer(expected=[8, 8, 8, 8],expected_return_value=4,param_index=2), '[6, 8, [11, 12, 10, 13]]', 2, None)

  @points(1)
  @name("test 15: truncate_and_count")
  def test_15(self):
      self.verify('truncate_and_count', answer.InlineAnswer(expected=[6, 7, 6, 7],expected_return_value=0,param_index=2), '[5, 8, [6, 7, 6, 7]]', 2, None)

  @points(1)
  @name("test 16: truncate_and_count")
  def test_16(self):
      self.verify('truncate_and_count', answer.InlineAnswer(expected=[],expected_return_value=0,param_index=2), '[5, 8, []]', 2, None)

