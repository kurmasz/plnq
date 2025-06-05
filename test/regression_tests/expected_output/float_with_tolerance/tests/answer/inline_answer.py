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
      return self.ordinals[self.param_index] if self.param_index <= 4 else f'{self.param_index}th'

    def display_expected_string(self):
      ordinal = self.ordinal_parameter()
      return f'modify the {ordinal} parameter to be `{self.display_expected_value()}`'

    def verify_value(self, observed):
        ordinal = self.ordinal_parameter()
        if self.expected == observed:
            return True
        if type(self.expected == str) or type(observed) == str:
            self.message_content = f'Expected the {ordinal} parameter to be modified to "{self.expected}", but was "{observed}"'
        else:
            self.message_content = f'Expected the {ordinal} parameter to be modified to {self.expected}, but was {observed}'
        return False
