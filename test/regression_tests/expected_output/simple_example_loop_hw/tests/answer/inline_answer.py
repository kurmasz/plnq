###############################################################################
#
# InlineAnswer
#
# Allows the answer to a PLNQ question to be a modified parameter rather 
# than a return value.
#
# IMPORTANT: expected_return_value is not used by InlineAnswer. For inline tests, 
# the expected return value is tested when main plnq script creates separate calls 
# to Test#verify for the modified parameter and the return value. 
# (c) 2023-2025 Anna Carvalho and Zachary Kurmas
#
###############################################################################

from . import Answer    

class InlineAnswer(Answer):
    
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

    def __init__(self, expected, expected_return_value=None, param_index=0):
        super().__init__(expected, strict=True, param_index=param_index)
        self.expected_return_value = expected_return_value

    def ordinal_parameter(self):
      return self.ordinals[self.param_index] if self.param_index <= 7 else f'{self.param_index -1}th'

    def display_expected_string(self):
      ordinal = self.ordinal_parameter()
      return f'modify the {ordinal} parameter to be `{self.display_expected_value()}`'

    def verify_value(self, observed):
        ordinal = self.ordinal_parameter()
        if self.expected == observed:
            return True
        exp_q = '"' if isinstance(self.expected, str) else ''
        obs_q = '"' if isinstance(observed, str) else ''
        self.message_content = f'Expected the {ordinal} parameter to be modified to {exp_q}{self.expected}{exp_q}, but was {obs_q}{observed}{obs_q}.'
        return False
