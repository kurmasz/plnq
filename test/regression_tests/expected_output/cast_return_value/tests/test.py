
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
  @name("test 1: is_standard_phone_number")
  def test_01(self):
      self.verify('is_standard_phone_number', False, '["16-231-4379"]', -1, bool)

  @points(1)
  @name("test 2: is_standard_phone_number")
  def test_02(self):
      self.verify('is_standard_phone_number', False, '["616-231-43789"]', -1, bool)

  @points(1)
  @name("test 3: is_standard_phone_number")
  def test_03(self):
      self.verify('is_standard_phone_number', False, '["800-THE-BOMB"]', -1, bool)

  @points(1)
  @name("test 4: is_standard_phone_number")
  def test_04(self):
      self.verify('is_standard_phone_number', False, '["(616)-331-5000"]', -1, bool)

  @points(1)
  @name("test 5: is_standard_phone_number")
  def test_05(self):
      self.verify('is_standard_phone_number', False, '["231-4514-7889"]', -1, bool)

  @points(1)
  @name("test 6: is_standard_phone_number")
  def test_06(self):
      self.verify('is_standard_phone_number', False, '["a231-451-7889"]', -1, bool)

  @points(1)
  @name("test 7: is_standard_phone_number")
  def test_07(self):
      self.verify('is_standard_phone_number', False, '["a31-451-7889"]', -1, bool)

  @points(1)
  @name("test 8: is_standard_phone_number")
  def test_08(self):
      self.verify('is_standard_phone_number', False, '["231-414-789"]', -1, bool)

  @points(1)
  @name("test 9: is_standard_phone_number")
  def test_09(self):
      self.verify('is_standard_phone_number', False, '["231-41a-7893"]', -1, bool)

  @points(1)
  @name("test 10: is_standard_phone_number")
  def test_10(self):
      self.verify('is_standard_phone_number', False, '["231-415-7b93"]', -1, bool)

  @points(1)
  @name("test 11: is_standard_phone_number")
  def test_11(self):
      self.verify('is_standard_phone_number', False, '["231-415-7293-"]', -1, bool)

  @points(1)
  @name("test 12: is_standard_phone_number")
  def test_12(self):
      self.verify('is_standard_phone_number', False, '["231-415-7293 "]', -1, bool)

  @points(1)
  @name("test 13: is_standard_phone_number")
  def test_13(self):
      self.verify('is_standard_phone_number', False, '[" 231-415-7293"]', -1, bool)

  @points(1)
  @name("test 14: is_standard_phone_number")
  def test_14(self):
      self.verify('is_standard_phone_number', False, '["231 415 7293"]', -1, bool)

  @points(1)
  @name("test 15: is_standard_phone_number")
  def test_15(self):
      self.verify('is_standard_phone_number', False, '["2314157293"]', -1, bool)

  @points(1)
  @name("test 16: is_paren_phone_number")
  def test_16(self):
      self.verify('is_paren_phone_number', True, '["(616)-231-4378"]', -1, bool)

  @points(1)
  @name("test 17: is_paren_phone_number")
  def test_17(self):
      self.verify('is_paren_phone_number', True, '["616-231-4379"]', -1, bool)

  @points(1)
  @name("test 18: is_paren_phone_number")
  def test_18(self):
      self.verify('is_paren_phone_number', False, '["616.231.4379"]', -1, bool)

  @points(1)
  @name("test 19: is_paren_phone_number")
  def test_19(self):
      self.verify('is_paren_phone_number', False, '["(616-231-4379"]', -1, bool)

  @points(1)
  @name("test 20: is_paren_phone_number")
  def test_20(self):
      self.verify('is_paren_phone_number', False, '["616)-231-4379"]', -1, bool)

  @points(1)
  @name("test 21: is_paren_phone_number")
  def test_21(self):
      self.verify('is_paren_phone_number', False, '["((616)-231-7789"]', -1, bool)

  @points(1)
  @name("test 22: is_paren_phone_number")
  def test_22(self):
      self.verify('is_paren_phone_number', False, '["(616-231)-9934"]', -1, bool)

  @points(1)
  @name("test 23: is_paren_phone_number")
  def test_23(self):
      self.verify('is_paren_phone_number', False, '["(616-231-9934)"]', -1, bool)

  @points(1)
  @name("test 24: is_paren_phone_number")
  def test_24(self):
      self.verify('is_paren_phone_number', False, '["(616-231-9934)"]', -1, bool)

  @points(1)
  @name("test 25: is_paren_phone_number")
  def test_25(self):
      self.verify('is_paren_phone_number', False, '["231-4514-7889"]', -1, bool)

  @points(1)
  @name("test 26: is_paren_phone_number")
  def test_26(self):
      self.verify('is_paren_phone_number', False, '["a231-451-7889"]', -1, bool)

  @points(1)
  @name("test 27: is_paren_phone_number")
  def test_27(self):
      self.verify('is_paren_phone_number', False, '["a31-451-7889"]', -1, bool)

  @points(1)
  @name("test 28: is_paren_phone_number")
  def test_28(self):
      self.verify('is_paren_phone_number', False, '["231-414-789"]', -1, bool)

  @points(1)
  @name("test 29: is_paren_phone_number")
  def test_29(self):
      self.verify('is_paren_phone_number', False, '["231-41a-7893"]', -1, bool)

  @points(1)
  @name("test 30: is_paren_phone_number")
  def test_30(self):
      self.verify('is_paren_phone_number', False, '["(231)-41a-7893"]', -1, bool)

  @points(1)
  @name("test 31: is_paren_phone_number")
  def test_31(self):
      self.verify('is_paren_phone_number', False, '["231-415-7b93"]', -1, bool)

  @points(1)
  @name("test 32: is_paren_phone_number")
  def test_32(self):
      self.verify('is_paren_phone_number', False, '["231-415-7293-"]', -1, bool)

  @points(1)
  @name("test 33: is_paren_phone_number")
  def test_33(self):
      self.verify('is_paren_phone_number', False, '["231-415-7293 "]', -1, bool)

  @points(1)
  @name("test 34: is_paren_phone_number")
  def test_34(self):
      self.verify('is_paren_phone_number', False, '[" 231-415-7293"]', -1, bool)

  @points(1)
  @name("test 35: is_paren_phone_number")
  def test_35(self):
      self.verify('is_paren_phone_number', False, '["231 415 7293"]', -1, bool)

  @points(1)
  @name("test 36: is_paren_phone_number")
  def test_36(self):
      self.verify('is_paren_phone_number', False, '["(231) 415 7293"]', -1, bool)

  @points(1)
  @name("test 37: is_paren_phone_number")
  def test_37(self):
      self.verify('is_paren_phone_number', False, '["(231)415 7293"]', -1, bool)

  @points(1)
  @name("test 38: is_paren_phone_number")
  def test_38(self):
      self.verify('is_paren_phone_number', False, '["(231)4157293"]', -1, bool)

  @points(1)
  @name("test 39: is_paren_phone_number")
  def test_39(self):
      self.verify('is_paren_phone_number', False, '["2314157222"]', -1, bool)

  @points(1)
  @name("test 40: is_dotted_phone_number")
  def test_40(self):
      self.verify('is_dotted_phone_number', True, '["(616)-231-4378"]', -1, bool)

  @points(1)
  @name("test 41: is_dotted_phone_number")
  def test_41(self):
      self.verify('is_dotted_phone_number', True, '["616-231-4379"]', -1, bool)

  @points(1)
  @name("test 42: is_dotted_phone_number")
  def test_42(self):
      self.verify('is_dotted_phone_number', True, '["616.231.4379"]', -1, bool)

  @points(1)
  @name("test 43: is_dotted_phone_number")
  def test_43(self):
      self.verify('is_dotted_phone_number', False, '["16-231-4379"]', -1, bool)

  @points(1)
  @name("test 44: is_dotted_phone_number")
  def test_44(self):
      self.verify('is_dotted_phone_number', False, '["616-231-43789"]', -1, bool)

  @points(1)
  @name("test 45: is_dotted_phone_number")
  def test_45(self):
      self.verify('is_dotted_phone_number', False, '["800-THE-BOMB"]', -1, bool)

  @points(1)
  @name("test 46: is_dotted_phone_number")
  def test_46(self):
      self.verify('is_dotted_phone_number', False, '["231-4514-7889"]', -1, bool)

  @points(1)
  @name("test 47: is_dotted_phone_number")
  def test_47(self):
      self.verify('is_dotted_phone_number', False, '["a231-451-7889"]', -1, bool)

  @points(1)
  @name("test 48: is_dotted_phone_number")
  def test_48(self):
      self.verify('is_dotted_phone_number', False, '["a31-451-7889"]', -1, bool)

  @points(1)
  @name("test 49: is_dotted_phone_number")
  def test_49(self):
      self.verify('is_dotted_phone_number', False, '["231-414-789"]', -1, bool)

  @points(1)
  @name("test 50: is_dotted_phone_number")
  def test_50(self):
      self.verify('is_dotted_phone_number', False, '["231-41a-7893"]', -1, bool)

  @points(1)
  @name("test 51: is_dotted_phone_number")
  def test_51(self):
      self.verify('is_dotted_phone_number', False, '["231-415-7b93"]', -1, bool)

  @points(1)
  @name("test 52: is_dotted_phone_number")
  def test_52(self):
      self.verify('is_dotted_phone_number', False, '["231-415-7293-"]', -1, bool)

  @points(1)
  @name("test 53: is_dotted_phone_number")
  def test_53(self):
      self.verify('is_dotted_phone_number', False, '["231-415-7293 "]', -1, bool)

  @points(1)
  @name("test 54: is_dotted_phone_number")
  def test_54(self):
      self.verify('is_dotted_phone_number', False, '[" 231-415-7293"]', -1, bool)

  @points(1)
  @name("test 55: is_dotted_phone_number")
  def test_55(self):
      self.verify('is_dotted_phone_number', False, '["231 415 7293"]', -1, bool)

  @points(1)
  @name("test 56: is_dotted_phone_number")
  def test_56(self):
      self.verify('is_dotted_phone_number', False, '["2314157293"]', -1, bool)

  @points(1)
  @name("test 57: is_dotted_phone_number")
  def test_57(self):
      self.verify('is_dotted_phone_number', False, '["231.4157293"]', -1, bool)

  @points(1)
  @name("test 58: is_dotted_phone_number")
  def test_58(self):
      self.verify('is_dotted_phone_number', False, '["231415.7293"]', -1, bool)

  @points(1)
  @name("test 59: is_dotted_phone_number")
  def test_59(self):
      self.verify('is_dotted_phone_number', True, '["(616)-231-6657"]', -1, bool)

  @points(1)
  @name("test 60: is_integer")
  def test_60(self):
      self.verify('is_integer', True, '["54323344"]', -1, bool)

  @points(1)
  @name("test 61: is_integer")
  def test_61(self):
      self.verify('is_integer', True, '["-4310"]', -1, bool)

  @points(1)
  @name("test 62: is_integer")
  def test_62(self):
      self.verify('is_integer', False, '["-.71"]', -1, bool)

  @points(1)
  @name("test 63: is_integer")
  def test_63(self):
      self.verify('is_integer', False, '["43a67"]', -1, bool)

  @points(1)
  @name("test 64: is_integer")
  def test_64(self):
      self.verify('is_integer', False, '["a"]', -1, bool)

  @points(1)
  @name("test 65: is_integer")
  def test_65(self):
      self.verify('is_integer', False, '["+b"]', -1, bool)

  @points(1)
  @name("test 66: is_integer")
  def test_66(self):
      self.verify('is_integer', False, '["55+16"]', -1, bool)

  @points(1)
  @name("test 67: is_integer")
  def test_67(self):
      self.verify('is_integer', False, '["55-16"]', -1, bool)

  @points(1)
  @name("test 68: is_integer")
  def test_68(self):
      self.verify('is_integer', False, '["55-"]', -1, bool)

  @points(1)
  @name("test 69: is_integer")
  def test_69(self):
      self.verify('is_integer', False, '["+-55"]', -1, bool)

  @points(1)
  @name("test 70: is_integer")
  def test_70(self):
      self.verify('is_integer', False, '["-+55"]', -1, bool)

  @points(1)
  @name("test 71: is_integer")
  def test_71(self):
      self.verify('is_integer', False, '["++55"]', -1, bool)

  @points(1)
  @name("test 72: is_integer")
  def test_72(self):
      self.verify('is_integer', False, '["--55"]', -1, bool)

  @points(1)
  @name("test 73: is_integer")
  def test_73(self):
      self.verify('is_integer', True, '["54323344"]', -1, bool)

  @points(1)
  @name("test 74: is_integer")
  def test_74(self):
      self.verify('is_integer', True, '["-4310"]', -1, bool)

  @points(1)
  @name("test 75: is_integer")
  def test_75(self):
      self.verify('is_integer', False, '["-.71"]', -1, bool)

  @points(1)
  @name("test 76: is_integer")
  def test_76(self):
      self.verify('is_integer', False, '["43a67"]', -1, bool)

  @points(1)
  @name("test 77: is_integer")
  def test_77(self):
      self.verify('is_integer', False, '["a"]', -1, bool)

  @points(1)
  @name("test 78: is_integer")
  def test_78(self):
      self.verify('is_integer', False, '["+b"]', -1, bool)

  @points(1)
  @name("test 79: is_integer")
  def test_79(self):
      self.verify('is_integer', False, '["55+16"]', -1, bool)

  @points(1)
  @name("test 80: is_integer")
  def test_80(self):
      self.verify('is_integer', False, '["55-16"]', -1, bool)

  @points(1)
  @name("test 81: is_integer")
  def test_81(self):
      self.verify('is_integer', False, '["55-"]', -1, bool)

  @points(1)
  @name("test 82: is_integer")
  def test_82(self):
      self.verify('is_integer', False, '["+-55"]', -1, bool)

  @points(1)
  @name("test 83: is_integer")
  def test_83(self):
      self.verify('is_integer', False, '["-+55"]', -1, bool)

  @points(1)
  @name("test 84: is_integer")
  def test_84(self):
      self.verify('is_integer', False, '["++55"]', -1, bool)

  @points(1)
  @name("test 85: is_integer")
  def test_85(self):
      self.verify('is_integer', False, '["--55"]', -1, bool)

  @points(1)
  @name("test 86: is_ip_address")
  def test_86(self):
      self.verify('is_ip_address', True, '["192.168.133.112"]', -1, bool)

  @points(1)
  @name("test 87: is_ip_address")
  def test_87(self):
      self.verify('is_ip_address', True, '["48.117.41.3"]', -1, bool)

  @points(1)
  @name("test 88: is_ip_address")
  def test_88(self):
      self.verify('is_ip_address', False, '["12.33.33"]', -1, bool)

  @points(1)
  @name("test 89: is_ip_address")
  def test_89(self):
      self.verify('is_ip_address', False, '["12..331.19"]', -1, bool)

  @points(1)
  @name("test 90: is_ip_address")
  def test_90(self):
      self.verify('is_ip_address', False, '[".221.222.333.121"]', -1, bool)

  @points(1)
  @name("test 91: is_ip_address")
  def test_91(self):
      self.verify('is_ip_address', False, '["192"]', -1, bool)

  @points(1)
  @name("test 92: is_ip_address")
  def test_92(self):
      self.verify('is_ip_address', False, '["192.168"]', -1, bool)

  @points(1)
  @name("test 93: is_ip_address")
  def test_93(self):
      self.verify('is_ip_address', False, '["192.168.221."]', -1, bool)

  @points(1)
  @name("test 94: is_ip_address")
  def test_94(self):
      self.verify('is_ip_address', False, '["192.21.112.88."]', -1, bool)

  @points(1)
  @name("test 95: is_ip_address")
  def test_95(self):
      self.verify('is_ip_address', True, '["0.0.0.0"]', -1, bool)

  @points(1)
  @name("test 96: is_ip_address")
  def test_96(self):
      self.verify('is_ip_address', True, '["1.2.3.4"]', -1, bool)

  @points(1)
  @name("test 97: is_ip_address")
  def test_97(self):
      self.verify('is_ip_address', False, '["22.33.abc.31"]', -1, bool)

  @points(1)
  @name("test 98: is_ip_address")
  def test_98(self):
      self.verify('is_ip_address', False, '["22.33.111.100a"]', -1, bool)

  @points(1)
  @name("test 99: is_ip_address")
  def test_99(self):
      self.verify('is_ip_address', False, '["b22.33.111.100"]', -1, bool)

