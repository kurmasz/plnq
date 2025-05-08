##########################################################
#
# Answer
#
############################################################
import math
import inspect
import re

class Answer:
    def __init__(self, expected, strict=True, param_index=-1):
        self.expected = expected
        self.strict = strict
        self.param_index = param_index

    def display_expected_value(self):
        return self.expected
    
    def display_expected_string(self):
        return f'return `{self.display_expected_value()}`'

    def verify_type(self, observed):
        if type(self.expected) != type(observed):
            self.message_content = f'Expected object of type {type(self.expected)}, but received {type(observed)} {observed}'
            return False
        return True

    def verify_value(self, observed):
        if self.expected == observed:
            return True
        if type(self.expected == str) or type(observed) == str:
            self.message_content = f'Expected "{self.expected}", but received "{observed}"'
        else:
            self.message_content = f'Expected {self.expected}, but received {observed}'
        return False

    def verify(self, observed):
        if self.strict and not self.verify_type(observed):
            return False
        return self.verify_value(observed)
        
    def message(self):
        return self.message_content
    
    def make(expected):
        if isinstance(expected, Answer):
            return expected
        if isinstance(expected, float):
            return FloatAnswer(expected)
        if isinstance(expected, re.Pattern):
            return ReAnswer(expected)
        return Answer(expected)
    
    def value_to_literal(value):
        if isinstance(value, str):
            return f"'{value}'"
        return value

    def constructor_string(self, package='answer'):
        param_strings = []
        for name, param in inspect.signature(self.__init__).parameters.items():
            if not param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                print("ERROR: Can only handle parameters that are POSITIONAL_OR_KEYWORD")
            value = getattr(self, param.name)
            param_strings.append(f'{name}={Answer.value_to_literal(value)}')
        return f'{package}.{self.__class__.__name__}({",".join(param_strings)})'


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
        4: 'fifth'
      }
      ordinal = ordinals[self.param_index] if self.param_index <= 4 else f'{self.param_index}th'
      return f'modify the {ordinal} parameter to be `{self.display_expected_value()}`'

