###############################################################################
#
# test_float_answer.py
#
# Unit tests for FloatAnswer
#
# (c) 2025 Zachary Kurmas
#
###############################################################################


import unittest
from plnq.answer import FloatAnswer 

class TestFloatAnswer(unittest.TestCase):

    def test_initialization(self):
        # Test default initialization
        answer = FloatAnswer(expected=3.14)
        self.assertEqual(answer.expected, 3.14)
        self.assertEqual(answer.rel_tol, 1e-09)
        self.assertEqual(answer.abs_tol, 0.0)
        self.assertTrue(answer.strict)

        # Test custom initialization
        answer = FloatAnswer(expected=3.14, rel_tol=1e-05, abs_tol=3e-05, strict=False)
        self.assertEqual(answer.expected, 3.14)
        self.assertEqual(answer.rel_tol, 1e-05)
        self.assertEqual(answer.abs_tol, 3e-05)
        self.assertFalse(answer.strict)

    def test_verify_value_within_tolerance(self):
        # Test when observed is within tolerance
        answer = FloatAnswer(expected=3.14, rel_tol=1e-05, abs_tol=1e-05)
        self.assertTrue(answer.verify_value(3.1400001))

        answer = FloatAnswer(expected=3.14, rel_tol=0.01)
        self.assertTrue(answer.verify_value(3.13))  # Within 1% tolerance

    def test_verify_value_outside_tolerance(self):
        # Test when observed is outside tolerance
        answer = FloatAnswer(expected=3.14, rel_tol=1e-09, abs_tol=0.0)
        self.assertFalse(answer.verify_value(3.15))
        self.assertEqual(answer.message_content, 'Expected 3.14, but received 3.15')

        answer = FloatAnswer(expected=3.14, rel_tol=0.01)
        self.assertFalse(answer.verify_value(3.12))  # Outside 1% tolerance
        self.assertEqual(answer.message_content, 'Expected 3.14, but received 3.12')

    def test_verify_value_absolute_tolerance(self):
        # Test with absolute tolerance
        answer = FloatAnswer(expected=3.14, abs_tol=0.1)
        self.assertTrue(answer.verify_value(3.239))  # Within absolute tolerance

        answer = FloatAnswer(expected=3.14, abs_tol=0.01)
        self.assertFalse(answer.verify_value(3.16))  # Outside absolute tolerance
        self.assertEqual(answer.message_content, 'Expected 3.14, but received 3.16')

if __name__ == '__main__':
    unittest.main()