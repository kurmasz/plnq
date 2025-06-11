###############################################################################
#
# test_autograde_verify_integration.py
#
# Integration tests for Test#verify from the Workbook's test.py
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

# Note: It's important to import answer with respect to 
# generated_dir2.  If you use plnq.answer, then the fully
# qualified name of the class will be plnq.answer.InlineAnswer, 
# and Answer.make will not work as expected.
from answer.inline_answer import InlineAnswer

class StudentCode:

    @staticmethod
    def two_x_plus_y(x, y):
        StudentCode.two_x_plus_y_called = True
        StudentCode.x_parm = x
        StudentCode.y_parm = y
        return 2*x + y

    @staticmethod
    def two_x_plus_y_missing_return(x, y):
        StudentCode.two_x_plus_y_called = True
        StudentCode.x_parm = x
        StudentCode.y_parm = y

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

    @staticmethod
    def sum_lists(lst1, coefficient, lst2):
        answer = []
        for i in range(len(lst1)):
            answer.append(lst1[i] * coefficient + lst2[i])
        return answer
    
    @staticmethod
    def increment_first_list(lst1, coefficient, lst2):
        for i in range(len(lst1)):
            lst1[i] = lst1[i] * coefficient + lst2[i]

    @staticmethod
    def increment_second_list(coefficient, lst1, lst2):
        for i in range(len(lst1)):
            lst2[i] = lst1[i] * coefficient + lst2[i]

    @staticmethod
    def increment_second_with_return(coefficient, lst1, lst2):
        for i in range(len(lst1)):
            lst2[i] = lst1[i] * coefficient + lst2[i]
        return sum(lst2)

class TestVerifyTest(unittest.TestCase):

    def setUp(self):
        Feedback.score = -999
        Feedback.message = None

        self.the_test = Test()
        self.the_test.st = StudentCode()

    def test_int_input_int_output_passes(self):
        self.the_test.verify(
            function_name='two_x_plus_y',
            expected=17,
            params_json='[5, 7]',
        )

        self.assertEqual(Feedback.score, 1)
        self.assertIsNone(Feedback.message)

    def test_int_input_int_output_incorrect_return_type(self):
        self.the_test.verify(
            function_name='two_x_plus_y',
            expected='17', # Note a string is expected not an int.
            params_json='[5, 7]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("two_x_plus_y(5, 7): Expected object of type <class 'str'>, but received <class 'int'> 17.", Feedback.message)

    def test_int_input_int_output_missing_return(self):
        self.the_test.verify(
            function_name='two_x_plus_y_missing_return',
            expected=17, # Note a string is expected not an int.
            params_json='[5, 7]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("two_x_plus_y_missing_return(5, 7): Expected object of type <class 'int'>, but received <class 'NoneType'> None.", Feedback.message)

    def test_int_input_int_output_incorrect_return_value(self):
        self.the_test.verify(
            function_name='two_x_plus_y',
            expected=19, # Note: This is not the correct answer, but it will generate the desired message.
            params_json='[5, 7]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("two_x_plus_y(5, 7): Expected 19, but received 17.", Feedback.message)

    #
    # No input string output tests
    #

    def test_no_input_string_output_passes(self):
        self.the_test.verify(
            function_name='return_hello',
            expected='Hello',
            params_json='[]',
        )

        self.assertEqual(Feedback.score, 1)
        self.assertIsNone(Feedback.message)

    def test_no_input_string_output_incorrect_return_type(self):
        self.the_test.verify(
            function_name='return_hello',
            expected=42,  # Note: An int is expected, not a string.
            params_json='[]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("return_hello(): Expected object of type <class 'int'>, but received <class 'str'> Hello.", Feedback.message)

    def test_no_input_string_output_incorrect_return_value(self):
        self.the_test.verify(
            function_name='return_hello',
            expected='the wrong thing',  # Note: This is not the correct answer, but it will generate the desired message.'
            params_json='[]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual('return_hello(): Expected "the wrong thing", but received "Hello".', Feedback.message)


    #
    # Two lists in, one list out tests
    def test_two_lists_in_one_list_out_passes(self):
        self.the_test.verify(
            function_name='sum_lists',
            expected=[4, 8, 12],
            params_json='[[1, 2, 3], 3, [1, 2, 3]]',
        )

        self.assertEqual(Feedback.score, 1)
        self.assertIsNone(Feedback.message)

    def test_two_lists_in_one_list_out_incorrect_return_type(self):
        self.the_test.verify(
            function_name='sum_lists',
            expected={0: 4, 1:8, 2:12},  # Note: A string is expected, not a list.
            params_json='[[1, 2, 3], 3, [1, 2, 3]]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("sum_lists([1, 2, 3], 3, [1, 2, 3]): Expected object of type <class 'dict'>, but received <class 'list'> [4, 8, 12].", Feedback.message)    

    def test_two_lists_in_one_list_out_incorrect_return_value(self):
        self.the_test.verify(
            function_name='sum_lists',
            expected=[4, 8, 13],  # Note: This is not the correct answer, but it will generate the desired message.
            params_json='[[1, 2, 3], 3, [1, 2, 3]]',
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("sum_lists([1, 2, 3], 3, [1, 2, 3]): Expected [4, 8, 13], but received [4, 8, 12].", Feedback.message)

    #
    # Modify first parameter.
    #
    def test_two_ints_modify_first_list_passes(self):
        self.the_test.verify(
            function_name='increment_first_list',
            expected=InlineAnswer(expected=[7, 11, 15], expected_return_value=None, param_index=0),
            params_json='[[1, 2, 3], 3, [4, 5, 6]]',
            param_index=0
        )
        self.assertEqual(Feedback.score, 1)
        self.assertIsNone(Feedback.message)


    def test_two_ints_modify_first_list_incorrect_modification_type(self):
        self.the_test.verify(
            function_name='increment_first_list',
            expected=InlineAnswer(expected='Good morning', expected_return_value=None, param_index=0), # Note: A list is expected, not string. 
            params_json='[[1, 2, 3], 3, [4, 5, 6]]',
            param_index=0
        )
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("increment_first_list([1, 2, 3], 3, [4, 5, 6]): Expected object of type <class 'str'>, but received <class 'list'> [7, 11, 15].", Feedback.message)


    def test_two_ints_modify_first_list_incorrect_return_value(self):
        self.the_test.verify(
            function_name='increment_first_list',

            # Note: This is not the correct answer, but it will generate the desired message
            expected=InlineAnswer(expected=[7, 11, 16], expected_return_value=None, param_index=0), # Note: A list is expected, not string. 
            params_json='[[1, 2, 3], 3, [4, 5, 6]]',
            param_index=0
        )

        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("increment_first_list([1, 2, 3], 3, [4, 5, 6]): Expected the first parameter to be modified to [7, 11, 16], but was [7, 11, 15].", Feedback.message)


    def test_first_param_to_modify_unchanged(self):
        self.the_test.verify(
            function_name='sum_lists',
            expected=InlineAnswer(expected=[13, 18, 22], expected_return_value=None, param_index=0),
            params_json='[[1, 2, 3], 3, [10, 12, 13]]',
            param_index=0  # This indicates that the first list should be modified.
        )
         
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("sum_lists([1, 2, 3], 3, [10, 12, 13]): Expected the first parameter to be modified to [13, 18, 22], but was [1, 2, 3].", Feedback.message)

    #
    # Modify last parameter.
    #
    def test_two_ints_modify_last_list_passes(self):
        self.the_test.verify(
            function_name='increment_second_list',
            expected=InlineAnswer(expected=[34, 38, 42], expected_return_value=None, param_index=2),
            params_json='[3, [10, 11, 12], [4, 5, 6]]',
            param_index=2
        )
        self.assertEqual(Feedback.score, 1)
        self.assertIsNone(Feedback.message)


    def test_two_ints_modify_last_list_incorrect_modification_type(self):
        self.the_test.verify(
            function_name='increment_second_list',
            expected=InlineAnswer(expected=413, expected_return_value=None, param_index=2), # Note: A list is expected, not string. 
            params_json='[3, [1, 2, 3], [4, 5, 6]]',
            param_index=2
        )
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("increment_second_list(3, [1, 2, 3], [4, 5, 6]): Expected object of type <class 'int'>, but received <class 'list'> [7, 11, 15].", Feedback.message)


    def test_two_ints_modify_last_list_incorrect_return_value(self):
        self.the_test.verify(
            function_name='increment_second_list',

            # Note: This is not the correct answer, but it will generate the desired message
            expected=InlineAnswer(expected=[7, 11, 16], expected_return_value=None, param_index=2), # Note: A list is expected, not string. 
            params_json='[3, [1, 2, 3], [4, 5, 6]]',
            param_index=2
        )
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("increment_second_list(3, [1, 2, 3], [4, 5, 6]): Expected the third parameter to be modified to [7, 11, 16], but was [7, 11, 15].", Feedback.message)


    def test_last_param_to_modify_unchanged(self):
        self.the_test.verify(
            function_name='sum_lists',
            expected=InlineAnswer(expected=[13, 18, 22], expected_return_value=None, param_index=2),
            params_json='[[1, 2, 3], 3, [10, 12, 13]]',
            param_index=2  # This indicates that the first list should be modified.
        )
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("sum_lists([1, 2, 3], 3, [10, 12, 13]): Expected the third parameter to be modified to [13, 18, 22], but was [10, 12, 13].", Feedback.message)

    #
    # Modified but wrong return value.
    #
    def test_two_ints_modify_second_list_with_return_passes(self):
        self.the_test.verify(
            function_name='increment_second_with_return',
            expected=InlineAnswer(expected=[34, 38, 42], expected_return_value=42, param_index=2),
            params_json='[3, [10, 11, 12], [4, 5, 6]]',
            param_index=2
        )
        self.assertEqual(Feedback.score, 1)
        self.assertIsNone(Feedback.message)

    def test_two_ints_modify_second_list_with_return_incorrect_return_type(self):
        self.the_test.verify(
            function_name='increment_second_with_return',
            expected=InlineAnswer(expected=[7, 11, 15], expected_return_value='Good Morning', param_index=2), # Note: An int is expected, not a string.
            params_json='[3, [1, 2, 3], [4, 5, 6]]',
            param_index=2
        )
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("increment_second_with_return(3, [1, 2, 3], [4, 5, 6]): Expected object of type <class 'str'>, but received <class 'int'> 42.", Feedback.message)

    def test_two_ints_modify_second_list_with_return_incorrect_return_value(self):
        self.the_test.verify(
            function_name='increment_second_with_return',

            # Note: This is not the correct answer, but it will generate the desired message
            expected=InlineAnswer(expected=[7, 11, 15], expected_return_value=43, param_index=2), # Note: An int is expected, not a string.
            params_json='[3, [1, 2, 3], [4, 5, 6]]',
            param_index=2
        )
        self.assertEqual(Feedback.score, 0)
        self.assertIsNotNone(Feedback.message)
        self.assertEqual("increment_second_with_return(3, [1, 2, 3], [4, 5, 6]): Expected return value to be 43, but was 42.", Feedback.message)

        
if __name__ == '__main__':
    unittest.main()