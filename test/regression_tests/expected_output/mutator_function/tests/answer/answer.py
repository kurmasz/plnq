###############################################################################
#
# Answer
#
# Encapsulates the answer to a PLNQ test case
#
# (c) 2023-2025 Anna Carvalho and Zachary Kurmas
#
###############################################################################
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
    
    @staticmethod
    def make(expected):
        from . import answer_types # lazy import to avoid circular imports
        if isinstance(expected, Answer):
            return expected
        if isinstance(expected, float):
            return answer_types['FloatAnswer'](expected)
        if isinstance(expected, re.Pattern):
            return answer_types['ReAnswer'](expected)
        return Answer(expected)
    
    @staticmethod 
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
            param_strings.append(f'{name}={self.value_to_literal(value)}')
        return f'{package}.{self.__class__.__name__}({",".join(param_strings)})'
