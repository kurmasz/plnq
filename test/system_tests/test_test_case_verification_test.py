###############################################################################
#
# test_case_verification_test.py
#
# Tests to verify that test case verification correctly reports errors.
#
# (c) 2025 Zachary Kurmas
#
###############################################################################


import system_test_base


class TestCaseVerificationTest(system_test_base.SystemTestBase):

    INCONSISTENT_TEST_CASES = 'Found inconsistent test cases.'

    def test_incorrect_expected_output(self):
        result = self.run_plnq(
            'simple_example_loop_incorrect_expected_output.ipynb', expect_empty_stderr=False)

        self.assertEqual(3, result.returncode)
        self.assertEqual(self.INCONSISTENT_TEST_CASES, result.stderr.strip())

        expected_output = [
            '!!! Test 1 letters_in_string(To be, or not to be: that is the question.): Expected 31, but received 30.',
            '!!! Test 4 letters_in_string(Fourscore and seven years ago): Expected 24, but received 25.'
        ]
        self.assertEqual(expected_output, result.stdout_lst)

    def test_incorrect_mutation(self):
        result = self.run_plnq(
            'mutator_function_with_incorrect_expected_mutation.ipynb', expect_empty_stderr=False)

        self.assertEqual(3, result.returncode)
        self.assertEqual(self.INCONSISTENT_TEST_CASES, result.stderr.strip())

        expected_output = [
            """!!! Test 0 remove_suffixes(['A', 'A', 'C', 'D']): Expected the first parameter to be modified to ['A', 'A', 'C+', 'D'], but was ['A', 'A', 'C', 'D'].""",
            """!!! Test 3 remove_suffixes([]): Expected the first parameter to be modified to ['C'], but was []."""
        ]
        self.assertEqual(expected_output, result.stdout_lst)

    def test_mutator_with_incorrect_return(self):
        result = self.run_plnq(
            'mutator_function_with_incorrect_expected_return.ipynb', expect_empty_stderr=False)

        self.assertEqual(3, result.returncode)
        self.assertEqual(self.INCONSISTENT_TEST_CASES, result.stderr.strip())

        expected_output = [
            '''!!! Test 0 (truncate_and_count)(0, ...) return value: Expected 2, but received 3.''',
            '''!!! Test 3 (truncate_and_count)(6, ...) return value: Expected object of type <class 'NoneType'>, but received <class 'int'> 4.'''
        ]
        self.assertEqual(expected_output, result.stdout_lst)


if __name__ == '__main__':
    import unittest
    unittest.main()
