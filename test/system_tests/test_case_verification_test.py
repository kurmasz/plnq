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

    def test_incorrect_expected_output(self):
        input_file = self.input_file(
            'simple_example_loop_incorrect_expected_output.ipynb')
        result = self.run_plnq(['--destroy', input_file, self.default_output])

        self.assertEqual(0, result.returncode)

        expected_output = [
            '!!! Test 1 letters_in_string(To be, or not to be: that is the question.): Expected "31", but received "30"',
            '!!! Test 4 letters_in_string(Fourscore and seven years ago): Expected "24", but received "25"'
        ]
        self.assertEqual(expected_output, result.stdout_lst)


if __name__ == '__main__':
    import unittest
    unittest.main()
