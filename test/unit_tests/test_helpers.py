###############################################################################
#
# helper_tests.py
#
# Unit tests for helper functions
#
# (c) 2024 Zachary Kurmas
#
###############################################################################

import sys
import unittest
import os

sys.path.append(os.path.dirname(__file__) + '/../..')
import plnq

class HelperTests(unittest.TestCase):

    #
    # Test determine_absolute_output_dir
    #

    def test_daor_single_component(self):
        observed = plnq.determine_absolute_output_dir("the_dir", "the_input.ipynb")
        self.assertEqual("thes_dir", observed)

    def test_daor_relative_path(self):
        observed = plnq.determine_absolute_output_dir("a/b/c/dir", "the_input.ipynb")
        self.assertEqual("a/b/c/dir", observed)

    def test_daor_absolute_path(self):
        observed = plnq.determine_absolute_output_dir("/a/b/c/dir", "the_input.ipynb")
        self.assertEqual("/a/b/c/dir", observed)

    def test_daor_relative_with_dash_single_input(self):
        observed = plnq.determine_absolute_output_dir("a/b/c/-", "the_input.ipynb")
        self.assertEqual("a/b/c/the_input", observed)

    def test_daor_relative_with_dash_relative_input(self):
        observed = plnq.determine_absolute_output_dir("a/b/c/-", "g/h/i/j/the_input.ipynb")
        self.assertEqual("a/b/c/the_input", observed)

    def test_daor_relative_with_dash_absolute_input(self):
        observed = plnq.determine_absolute_output_dir("a/b/c/-", "/g/h/i/j/the_input.ipynb")
        self.assertEqual("a/b/c/the_input", observed)

    def test_daor_relative_with_dash_obnoxious_input1(self):
        observed = plnq.determine_absolute_output_dir("a/b/c/-", "g/why.ipynb/i/j/the_input.ipynb")
        self.assertEqual("a/b/c/the_input", observed)

    def test_daor_non_ipynb_raises_exception1(self):
        with self.assertRaises(ValueError):
            plnq.determine_absolute_output_dir("a/b/c", "the_input")  

    def test_daor_non_ipynb_raises_exception2(self):
        with self.assertRaises(ValueError):
            plnq.determine_absolute_output_dir("a/b/c", "g/why.ipynb/i/j/the_input")  

    def test_daor_non_ipynb_raises_exception2(self):
        with self.assertRaises(ValueError):
            plnq.determine_absolute_output_dir("a/b/c/-", "g/why.ipynb/i/j/the_input")      

if __name__ == '__main__':
    unittest.main()