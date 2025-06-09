###############################################################################
#
# test_inline_answer.py
#
# Unit tests for InlineAnswer
#
# (c) 2025 Zachary Kurmas
#
###############################################################################

import unittest
from plnq.answer import InlineAnswer  # Replace with the actual module name

class TestInlineAnswer(unittest.TestCase):

    def test_initialization(self):
        ia = InlineAnswer(expected=42, expected_return_value=100, param_index=2)
        self.assertEqual(ia.expected, 42)
        self.assertEqual(ia.expected_return_value, 100)
        self.assertEqual(ia.param_index, 2)
        self.assertTrue(ia.strict)

    def test_ordinal_parameter_basic(self):
        test_cases = [
            (0, 'first'),
            (1, 'second'),
            (2, 'third'),
            (3, 'fourth'),
            (4, 'fifth'),
            (5, 'sixth'),
            (6, 'seventh'),
            (7, 'eighth'),
            (10, '9th'),
            (11, '10th'),
            (20, '19th'),
            (100, '99th')
        ]
        for index, expected_ordinal in test_cases:
            with self.subTest(index=index):
                ia = InlineAnswer(expected=0, param_index=index)
                self.assertEqual(ia.ordinal_parameter(), expected_ordinal)

    def test_display_expected_string_with_int(self):
        ia = InlineAnswer(expected=42, param_index=1)
        self.assertEqual(ia.display_expected_string(), "modify the second parameter to be `42`")

    def test_display_expected_string_with_string(self):
        ia = InlineAnswer(expected='Michigan', param_index=2)
        self.assertEqual(ia.display_expected_string(), 'modify the third parameter to be `Michigan`')


    def test_verify_value_match(self):
        ia = InlineAnswer(expected=10, param_index=0)
        self.assertTrue(ia.verify_value(10))

    def test_verify_value_mismatch_numbers(self):
        ia = InlineAnswer(expected=42, param_index=3)
        self.assertFalse(ia.verify_value(99))
        self.assertEqual(
            ia.message_content,
            "Expected the fourth parameter to be modified to 42, but was 99."
        )

    def test_verify_value_mismatch_strings(self):
        ia = InlineAnswer(expected="hello", param_index=2)
        self.assertFalse(ia.verify_value("world"))
        self.assertEqual(
            ia.message_content,
            'Expected the third parameter to be modified to "hello", but was "world".'
        )

if __name__ == '__main__':
    unittest.main()
