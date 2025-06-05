###############################################################################
#
# system_test_base.py
#
#
# (c) 2025 Zachary Kurmas
#
###############################################################################

import unittest
import os
import sys
import re
import subprocess
import plnq

class SystemTestBase(unittest.TestCase):

    # PLNQ_VERSION_STRING = f'plnq v2.0.1'
    PLNQ_VERSION_STRING = f'plnq v{plnq.PLNQ_VERSION}'

    # Get the absolute path to the project root (2 levels up from this file)
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../..'))

    input_directory = os.path.join(os.path.dirname(__file__), 'input')

    default_output_base = os.path.join(os.path.dirname(__file__), 'output')
    default_output =os.path.join(default_output_base, '-')

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.default_output_base):
            os.makedirs(cls.default_output_base)    

    def input_file(self, filename):
        return os.path.join(self.input_directory, filename)

    #
    # IMPORTANT: stdout_lst does not contain the version string
    #
    def run_plnq(self, parameters, expect_empty_stderr=True):

        if type(parameters) == str:
            input_file = self.input_file(parameters)
            parameters = ['--destroy', input_file, self.default_output]

        result = subprocess.run([sys.executable, '-m', 'plnq'] + parameters,
                                # env={**os.environ, 'PYTHONPATH': project_root},
                                cwd=self.project_root,
                                capture_output=True, text=True)

        if expect_empty_stderr:
            self.assertEqual('', result.stderr)
        else:
            result.stderr_lst = result.stderr.splitlines()

        lines = result.stdout.splitlines()
        self.assertEqual(f"{self.PLNQ_VERSION_STRING}", lines[0])
        result.stdout_lst = lines[1:]
        return result

    @staticmethod
    def remove_whitespace(str):
        return re.sub(r'\s+', '', str)

    def assertEqualIgnoreWhitespace(self, expected, observed):
        norm_expected = self.remove_whitespace(expected)
        norm_observed = self.remove_whitespace(observed)
        if norm_expected != norm_observed:
            msg = (
                "Strings are not equal ignoring whitespace:\n"
                f"Expected (original): {repr(expected)}\n"
                f"Observed (original): {repr(observed)}\n"
                f"Expected (no whitespace): {repr(norm_expected)}\n"
                f"Observed (no whitespace): {repr(norm_observed)}"
            )
            raise self.failureException(msg)
