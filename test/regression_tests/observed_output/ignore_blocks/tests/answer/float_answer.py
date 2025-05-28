###############################################################################
#
# FloatAnswer
#
# Encapsulates a floating-point answer to a PLNQ test case (e.g., allows the 
# user to specify the desired tolerance).
#
# (c) 2023-2025 Anna Carvalho and Zachary Kurmas
#
###############################################################################

from . import Answer
import math

class FloatAnswer(Answer):
    def __init__(self, expected, rel_tol=1e-09, abs_tol=0.0, strict=True):
        super().__init__(expected, strict=strict)
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def verify_value(self, observed):
        if math.isclose(self.expected, observed, rel_tol=self.rel_tol, abs_tol=self.abs_tol):
            return True
        self.message_content = f'Expected {self.expected}, but received {observed}'
        return False