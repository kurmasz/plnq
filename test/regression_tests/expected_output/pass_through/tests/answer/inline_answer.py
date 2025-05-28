###############################################################################
#
# InlineAnswer
#
# Allows the answer to a PLNQ question to be a modified parameter rather 
# than a return value.
#
# (c) 2023-2025 Anna Carvalho and Zachary Kurmas
#
###############################################################################

from . import Answer    

class InlineAnswer(Answer):
    def __init__(self, expected, expected_return_value=None, param_index=0):
        super().__init__(expected, strict=True, param_index=param_index)
        self.expected_return_value = expected_return_value

    def display_expected_string(self):
      ordinals = {
        0: 'first',
        1: 'second',
        2: 'third',
        3: 'fourth',
        4: 'fifth',
        5: 'sixth',
        6: 'seventh',
        7: 'eighth'
      }
      ordinal = ordinals[self.param_index] if self.param_index <= 4 else f'{self.param_index}th'
      return f'modify the {ordinal} parameter to be `{self.display_expected_value()}`'

