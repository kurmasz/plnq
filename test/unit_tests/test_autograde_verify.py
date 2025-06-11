###############################################################################
#
# test_autograde_verify.py
#
# Unit tests for Test#verify from the Workbook's test.py
#
# (c) 2025 Zachary Kurmas
#
###############################################################################
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Since we don't know the cwd of the process that will run this test, we need to
# dynamically add the path to the generated directory where the mock_pl module is located.
generated_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'mock_pl'))
sys.path.insert(0, generated_dir)

generated_dir2 = os.path.abspath(os.path.join(os.path.dirname(
    __file__), '..', '..', 'plnq', 'quiz_template', 'tests'))
sys.path.insert(0, generated_dir2)

from code_feedback import Feedback
from test import Test

class StudentCode:

    @staticmethod
    def two_x_plus_y(x, y):
        StudentCode.two_x_plus_y_called = True
        StudentCode.x_parm = x
        StudentCode.y_parm = y
        return 2*x + y

    @staticmethod
    def three_x_minus_y(x, y):
        StudentCode.three_x_minus_y_called = True
        StudentCode.x_parm = x
        StudentCode.y_parm = y
        return 3*x - y

    @staticmethod
    def return_hello():
        StudentCode.return_hello_called = True
        StudentCode.x_parm = -999
        StudentCode.y_parm = -777
        return "Hello"


class TestVerifyTest(unittest.TestCase):

    def setUp(self):
        Feedback.score = -999
        Feedback.message = None

        # Reset static variables in StudentCode
        StudentCode.two_x_plus_y_called = False
        StudentCode.three_x_minus_y_called = False
        StudentCode.return_hello_called = False
        StudentCode.x_parm = -999
        StudentCode.y_parm = -777

        self.the_test = Test()
        self.the_test.st = StudentCode()


    def test_verify_calls_named_function(self):

        self.the_test.verify(
            function_name='two_x_plus_y',
            expected=17,
            params_json='[5, 7]',
        )

        self.assertTrue(StudentCode.two_x_plus_y_called)
        self.assertFalse(StudentCode.three_x_minus_y_called)
        self.assertFalse(StudentCode.return_hello_called)

        self.assertEqual(StudentCode.x_parm, 5)
        self.assertEqual(StudentCode.y_parm, 7)

    def test_verify_calls_named_function_with_no_params(self):

        self.the_test.verify(
            function_name='return_hello',
            expected='hello',
            params_json='[]',
        )

        self.assertFalse(StudentCode.two_x_plus_y_called)
        self.assertFalse(StudentCode.three_x_minus_y_called)
        self.assertTrue(StudentCode.return_hello_called)
        self.assertEqual(StudentCode.x_parm, -999)
        self.assertEqual(StudentCode.y_parm, -777)

    def test_call_cast_if_not_None(self):

        cast_param = None

        def the_cast(x):
            nonlocal cast_param
            cast_param = x
            return x
        
        self.the_test.verify(
            function_name='three_x_minus_y',
            expected=8,
            params_json='[5, 7]',
            cast=the_cast
        )

        self.assertEqual(cast_param, 8)


    @patch('answer.Answer.make')
    def test_answer_make_called_with_expected(self, mock_make):

        # Mock Answer instance and its verify method
        mock_answer_instance = MagicMock()
        mock_answer_instance.verify.return_value = True
        mock_make.return_value = mock_answer_instance

        expected_value = 42
        self.the_test.verify('three_x_minus_y', expected_value, '[10,8]')

        # Assert
        mock_make.assert_called_once_with(expected_value)

    @patch('answer.Answer.make')
    def test_answer_calls_verify_with_return_value_by_default(self, mock_make):
        # Mock Answer instance and its verify method
        mock_verifier = MagicMock()
        mock_verifier.verify.return_value = True
        mock_make.return_value = mock_verifier

        expected_value = 42
        self.the_test.verify('three_x_minus_y', expected_value, '[10,8]', param_index=-1)

        # Assert
        mock_verifier.verify.assert_called_once_with(22)

    @patch('answer.Answer.make')
    def test_answer_calls_verify_with_return_value_by_default(self, mock_make):
        # Mock Answer instance and its verify method
        mock_verifier = MagicMock()
        mock_verifier.verify.return_value = True
        mock_make.return_value = mock_verifier


        expected_value = 42
        self.the_test.verify('three_x_minus_y', expected_value, '[10,8]')

        # Assert
        mock_verifier.verify.assert_called_once_with(22)

    @patch('answer.Answer.make')
    def test_answer_calls_verify_with_return_value_by_when_param_index_neg1(self, mock_make):
        # Mock Answer instance and its verify method
        mock_verifier = MagicMock()
        mock_verifier.verify.return_value = True
        mock_make.return_value = mock_verifier

        expected_value = 42
        self.the_test.verify('three_x_minus_y', expected_value, '[15,12]', param_index=-1)

        # Assert
        mock_verifier.verify.assert_called_once_with(33)

    @patch('answer.Answer.make')
    def test_answer_calls_verify_with_return_value_by_when_given_param_index0(self, mock_make):
        # Mock Answer instance and its verify method
        mock_verifier = MagicMock()
        mock_verifier.verify.return_value = True
        mock_make.return_value = mock_verifier

        expected_value = 42
        self.the_test.verify('three_x_minus_y', expected_value, '[15,12]', param_index=0)

        # Assert
        mock_verifier.verify.assert_called_once_with(15)


    @patch('answer.Answer.make')
    def test_answer_calls_verify_with_return_value_by_when_given_param_index1(self, mock_make):
        # Mock Answer instance and its verify method
        mock_verifier = MagicMock()
        mock_verifier.verify.return_value = True
        mock_make.return_value = mock_verifier

        expected_value = 42
        self.the_test.verify('three_x_minus_y', expected_value, '[15,12]', param_index=1)

        # Assert
        mock_verifier.verify.assert_called_once_with(12)

    def test_score_set_to_1_when_verifier_passes(self):

        expected_value = 33
        self.the_test.verify('three_x_minus_y', expected_value, '[15,12]')

        self.assertEqual(Feedback.score, 1)

    def test_score_set_to_0_when_verifier_fails(self):

        expected_value = 32 # not the correct answer
        self.the_test.verify('three_x_minus_y', expected_value, '[15,12]')

        self.assertEqual(Feedback.score, 0)

    def test_feedback_added_when_verifier_fails(self):

        expected_value = 32 # not the correct answer
        self.the_test.verify('three_x_minus_y', expected_value, '[15,12]')

        self.assertEqual(Feedback.message, "three_x_minus_y(15,12): Expected 32, but received 33.")


if __name__ == '__main__':
    unittest.main()
