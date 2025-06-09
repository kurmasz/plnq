###############################################################################
#
# test_answer_constructor_string.py
#
# Unit tests for Answer.constructor_string
#
# (c) 2025 Zachary Kurmas
#
###############################################################################

import unittest
from unittest.mock import patch
import inspect
from plnq.answer import Answer, FloatAnswer

class TestAnswerConstructorString(unittest.TestCase):

    def test_constructor_string_default_package(self):
        # Test constructor_string with default package
        answer = Answer(expected=42, strict=True, param_index=-1)
        expected_string = "answer.Answer(expected=42,strict=True,param_index=-1)"
        self.assertEqual(answer.constructor_string(), expected_string)

    def test_constructor_default_Answer_params(self):
        # Test constructor_string with default package
        answer = Answer(expected=91)
        expected_string = "answer.Answer(expected=91,strict=True,param_index=-1)"
        self.assertEqual(answer.constructor_string(), expected_string)

    def test_constructor_string_custom_package(self):
        # Test constructor_string with a custom package name
        answer = Answer(expected="test", strict=False, param_index=2)
        expected_string = "custom_package.Answer(expected='test',strict=False,param_index=2)"
        self.assertEqual(answer.constructor_string(package='custom_package'), expected_string)

    def test_constructor_string_with_list(self):
        # Test constructor_string with various parameter types
        answer = Answer(expected=[1, 2, 3], strict=False, param_index=5)
        expected_string = "answer.Answer(expected=[1, 2, 3],strict=False,param_index=5)"
        self.assertEqual(answer.constructor_string(), expected_string)

    def test_constructor_string_with_dict(self):
        # Test constructor_string with various parameter types
        answer = Answer(expected={'george': 'jones'}, strict=False, param_index=5)
        expected_string = "answer.Answer(expected={'george': 'jones'},strict=False,param_index=5)"
        self.assertEqual(answer.constructor_string(), expected_string)

    def test_constructor_string_FloatAnswer(self):
        # Test constructor_string with default package
        answer = FloatAnswer(expected=4.232, abs_tol=2e-5, strict=True)
        expected_string = "answer.FloatAnswer(expected=4.232,rel_tol=1e-09,abs_tol=2e-05,strict=True)"
        self.assertEqual(answer.constructor_string(), expected_string)


    # TODO: I don't remember why I needed this check for POSITIONAL_OR_KEYWORD
    # so, this test is inactive.
    def xx_test_constructor_string_error_handling(self):
        # Test constructor_string error handling for unsupported parameter kinds
        class UnsupportedParamKind:
            def __init__(self, *args):  # Using VAR_POSITIONAL to trigger an error
                pass

        unsupported = UnsupportedParamKind()

        with patch('inspect.signature') as mock_signature:
            # Mocking the signature to return a parameter kind that is not handled
            mock_signature.return_value = inspect.Signature([
                inspect.Parameter('args', inspect.Parameter.VAR_POSITIONAL)
            ])

            with self.assertLogs(level='ERROR') as log:
                unsupported_constructor_string = Answer.constructor_string(unsupported)
                self.assertIn("ERROR: Can only handle parameters that are POSITIONAL_OR_KEYWORD", log.output)

if __name__ == '__main__':
    unittest.main()