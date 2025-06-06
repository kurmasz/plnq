###############################################################################
#
# test_suite_test.py
#
# Tests to verify that the auto-generated test suite works correctly.
#
# (c) 2025 Zachary Kurmas
#
###############################################################################

import unittest
import os
import sys


generated_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mock_pl'))
sys.path.insert(0, generated_dir)

generated_dir2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'regression_tests', 'expected_output', 'simple_example_loop_hw', 'tests'))
sys.path.insert(0, generated_dir2)

from test import Test
from code_feedback import Feedback

class StudentCode:
    @staticmethod
    def letters_in_string(str):
        return 14

class TestSuiteTest(unittest.TestCase):

    def test_example1(self):
        the_test = Test()
        the_test.st = StudentCode()

        the_test.test_01()

        print(Feedback.message)

if __name__ == '__main__':
    unittest.main()     
