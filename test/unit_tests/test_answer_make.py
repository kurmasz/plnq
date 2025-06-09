###############################################################################
#
# test_answer_make.py
#
# Unit tests for Answer.make
#
# (c) 2024 Zachary Kurmas
#
###############################################################################

import re
import unittest
from unittest.mock import patch, Mock
from plnq.answer import Answer, FloatAnswer

class AnswerMakeTest(unittest.TestCase):

    def test_make_with_answer_instance(self):
        original_answer = Answer(42)
        result = Answer.make(original_answer)
        self.assertIs(result, original_answer)

    def test_make_with_answer_subclass(self):
        original_answer = FloatAnswer(8.675309411)
        result = Answer.make(original_answer)
        self.assertIs(result, original_answer)

    @patch('plnq.answer.answer_types', new_callable=lambda: {"FloatAnswer": Mock()})
    def test_make_with_float(self, mock_answer_types):
        float_value = 3.14
        float_answer_mock = mock_answer_types['FloatAnswer']
        result = Answer.make(float_value)
        float_answer_mock.assert_called_once_with(float_value)
        self.assertEqual(result, float_answer_mock.return_value)

    @patch('plnq.answer.answer_types', new_callable=lambda: {"ReAnswer": Mock()})
    def test_make_with_regex(self, mock_answer_types):
        pattern = re.compile(r'\d+')
        re_answer_mock = mock_answer_types['ReAnswer']
        result = Answer.make(pattern)
        re_answer_mock.assert_called_once_with(pattern)
        self.assertEqual(result, re_answer_mock.return_value)

    def test_make_with_string(self):
        expected_value = "some string"
        result = Answer.make(expected_value)
        self.assertIsInstance(result, Answer)
        self.assertEqual(result.expected, expected_value)

    def test_make_with_int(self):
        expected_value = 41
        result = Answer.make(expected_value)
        self.assertIsInstance(result, Answer)
        self.assertEqual(result.expected, expected_value)

    def test_make_with_list(self):
        expected_value = [8, 6, 7, 5, 3, 0, 9]
        result = Answer.make(expected_value)
        self.assertIsInstance(result, Answer)
        self.assertEqual(result.expected, expected_value)

    def test_make_with_list(self):
        expected_value = {"key": "value", "yin": "yang"}
        result = Answer.make(expected_value)
        self.assertIsInstance(result, Answer)
        self.assertEqual(result.expected, expected_value)

if __name__ == '__main__':
    unittest.main()