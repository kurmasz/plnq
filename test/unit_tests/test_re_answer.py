###############################################################################
#
# test_re_answer.py
#
# Unit tests for ReAnswer
#
# (c) 2025 Zachary Kurmas
#
###############################################################################

from plnq.answer.re_answer import ReAnswer
import unittest
import re

class TestReAnswer(unittest.TestCase):
    def test_initialization_with_string(self):
        pattern = r'\d+'
        re_answer = ReAnswer(pattern)
        self.assertIsInstance(re_answer.expected, re.Pattern)
        self.assertEqual(re_answer.expected.pattern, pattern)

    def test_initialization_with_pattern(self):
        pattern = re.compile(r'\d+')
        re_answer = ReAnswer(pattern)
        self.assertEqual(re_answer.expected, pattern)

    def test_initialization_default_alt_answer(self):
        pattern = r'\de(d\+)'
        re_answer = ReAnswer(pattern)
        self.assertIsNone(re_answer.alt_answer)

    def test_initialization_with_alt_answer(self):
        pattern = r'a(bcd)+e'
        alt_answer = "Say hello!"
        re_answer = ReAnswer(pattern, alt_answer=alt_answer)
        self.assertEqual(re_answer.alt_answer, alt_answer)

    #
    # Test verify_type method
    #

    def test_verify_type_with_string(self):
        re_answer = ReAnswer(r'(1|3|5|7|9)+')
        self.assertTrue(re_answer.verify_type("world"))

    def test_verify_type_with_int(self):
        re_answer = ReAnswer(r'(1|3|5|7|9)abc')
        self.assertFalse(re_answer.verify_type(123))
        self.assertEqual("Expected a string, but received <class 'int'> 123", re_answer.message_content)

    def test_verify_type_with_list(self):
        re_answer = ReAnswer(r'(1|3|5|7|9)abc')
        self.assertFalse(re_answer.verify_type([3, 5, 8]))
        self.assertEqual("Expected a string, but received <class 'list'> [3, 5, 8]", re_answer.message_content)


    #
    # Test verify_value method
    #

    def test_verify_value_matching(self):
        re_answer = ReAnswer(r'(3|5|7)+')
        self.assertTrue(re_answer.verify_value("33735773"))

        re_answer = ReAnswer(r'(3|5|7)+')
        self.assertTrue(re_answer.verify_value("xxx33735773xxx"))

        re_answer = ReAnswer(r'^(3|5|7)+$')
        self.assertTrue(re_answer.verify_value("375337773573"))

    def test_verify_value_not_matching(self):
        re_answer = ReAnswer(r'^(3|5|7)+$')
        self.assertFalse(re_answer.verify_value("37337273537"))
        self.assertEqual("Expected 37337273537 to match /^(3|5|7)+$/", re_answer.message_content)

    #
    # Test display_expected_value method
    #

    def test_display_expected_value_with_alt_answer(self):
        re_answer = ReAnswer("hello", alt_answer="Say hello!")
        self.assertEqual("Say hello!", re_answer.display_expected_value())

    def test_display_expected_value_without_alt_answer(self):
        re_answer = ReAnswer(r'(a|b|c)*d(e|f|g)+')
        self.assertEqual(r'(a|b|c)*d(e|f|g)+', re_answer.display_expected_value())

# Run the unit tests
if __name__ == "__main__":
    unittest.main()