###############################################################################
#
# ReAnswer
#
# Encapsulates a regular expression answer to a PLNQ test case.
#
# (c) 2023-2025 Anna Carvalho and Zachary Kurmas
#
###############################################################################

from . import Answer
import re

class ReAnswer(Answer):
    def __init__(self, expected, alt_answer=None):

        # If present, display the alt_answer as the expected value, rather than the 
        # regular expression.
        self.alt_answer = alt_answer
        if isinstance(expected, str):
            super().__init__(re.compile(expected), strict=True)
        else:
            super().__init__(expected, strict=True)

    def verify_type(self, observed):
        if type(observed) != str:
            self.message_content = f'Expected object of type {type("str")}, but received {type(observed)} {observed}'
            return False
        return True

    def verify_value(self, observed):
        if self.expected.search(observed):
            return True
        self.message_content = f'Expected {observed} to match {self.expected}'
        return False
    
    def display_expected_value(self):
        if self.alt_answer != None:
            return self.alt_answer
        else:
            return super().display_expected_value()