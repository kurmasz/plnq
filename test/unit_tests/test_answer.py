###############################################################################
#
# test_answer.py
#
# Unit tests for Answer
#
# (c) 2025 Zachary Kurmas
#
###############################################################################

import unittest
from plnq.answer import Answer

class Animal:
    pass
        
class Dog(Animal):
    def __str__(self):
        return "I am a dog"

class AnswerTest(unittest.TestCase):
    def test_init_default(self):
        # Test initialization with default values
        answer = Answer(expected=42)
        self.assertEqual(answer.expected, 42)
        self.assertTrue(answer.strict)
        self.assertEqual(answer.param_index, -1)
        
    def test_init_non_default(self):
        # Test initialization with non-default values
        answer = Answer(expected="test", strict=False, param_index=2)
        self.assertEqual(answer.expected, "test")
        self.assertFalse(answer.strict)
        self.assertEqual(answer.param_index, 2)
    
    #
    # display_expected_value tests
    #

    def test_display_expected_value(self):
        # Test display_expected_value method
        answer = Answer(expected=42)
        self.assertEqual(answer.display_expected_value(), 42)

        answer = Answer(expected="expected string")
        self.assertEqual(answer.display_expected_value(), "expected string")

    #
    # display_expected_string tests
    #

    def test_display_expected_string(self):
        # Test display_expected_string method
        answer = Answer(expected=42)
        self.assertEqual(answer.display_expected_string(), "return `42`")

        answer = Answer(expected="expected string")
        self.assertEqual(answer.display_expected_string(), "return `expected string`")


    #
    # verify_type tests
    #

    def test_verify_type_matching_types(self):
        # Test when types match
        answer = Answer(expected=42)
        self.assertTrue(answer.verify_type(100))  # Both are integers

        answer = Answer(expected="test")
        self.assertTrue(answer.verify_type("another string"))  # Both are strings

        answer = Answer(expected=[1, 2, 3])
        self.assertTrue(answer.verify_type([4, 5, 6]))  # Both are lists

    def test_verify_type_expected_None(self):
        # Test when expected is None
        answer = Answer(expected=None)
        self.assertTrue(answer.verify_type(None))

    def test_verify_type_non_matching_types(self):
        # Test when types do not match
        answer = Answer(expected=42)
        self.assertFalse(answer.verify_type("string"))
        self.assertEqual(
            answer.message_content, 
            'Expected object of type <class \'int\'>, but received <class \'str\'> string.'
        )

        answer = Answer(expected="test")
        self.assertFalse(answer.verify_type(42))
        self.assertEqual(
            answer.message_content, 
            'Expected object of type <class \'str\'>, but received <class \'int\'> 42.'
        )

        answer = Answer(expected=[1, 2, 3])
        self.assertFalse(answer.verify_type((4, 5, 6)))  # List vs tuple
        self.assertEqual(
            answer.message_content, 
            'Expected object of type <class \'list\'>, but received <class \'tuple\'> (4, 5, 6).'
        )

    # This method checks exact type. Thus, checking an instance
    # of a subclass will fail. I don't believe that this failure is 
    # important to the operation of plnq; but, I include the test case
    # here to document the existing behavior.
    #
    # ?P<mod> is a named capture group.
    # ?P=mod is a backreference to the capture group named mod.

    def test_verify_type_parent_and_child(self):
        answer = Answer(expected=Animal())
        self.assertFalse(answer.verify_type(Dog()))

        pattern = (
            r"Expected object of type <class '(?P<mod>[\w\.]+)\.Animal'>, "
            r"but received <class '(?P=mod)\.Dog'> I am a dog."
        )
        self.assertRegex(answer.message_content, pattern)



    def test_verify_type_unexpected_None(self):
        # Test when observed is None
        answer = Answer(expected=42)
        self.assertFalse(answer.verify_type(None))
        self.assertEqual(
            answer.message_content, 
            'Expected object of type <class \'int\'>, but received <class \'NoneType\'> None.'
        )

    def test_verify_type_unexpected_non_None(self):
        # Test when expected is None
        answer = Answer(expected=None)
        self.assertFalse(answer.verify_type(42))
        self.assertEqual(
            answer.message_content, 
            'Expected object of type <class \'NoneType\'>, but received <class \'int\'> 42.'
        )


    #
    # verify_value tests
    #

    def test_verify_value_matching_values(self):
        # Test when values match
        answer = Answer(expected=42)
        self.assertTrue(answer.verify_value(42))  # Both values are 42

        answer = Answer(expected="test")
        self.assertTrue(answer.verify_value("test"))  # Both strings are identical

        answer = Answer(expected=[1, 2, 3])
        self.assertTrue(answer.verify_value([1, 2, 3]))  # Both lists are identical

        answer = Answer(expected={"foo": "bar"})
        self.assertTrue(answer.verify_value({"foo": "bar"}))  # Both dicts are identical    

    def test_verify_value_non_matching_ints(self):
        # Test when values do not match
        answer = Answer(expected=42)
        self.assertFalse(answer.verify_value(100))
        self.assertEqual(
            answer.message_content,
            'Expected 42, but received 100.'
        )

    def test_verify_value_non_matching_strings(self):
        answer = Answer(expected="test")
        self.assertFalse(answer.verify_value("different"))
        self.assertEqual(
            answer.message_content,
            'Expected "test", but received "different".'
        )

    def test_verify_value_non_matching_lists(self):
        answer = Answer(expected=[1, 2, 3])
        self.assertFalse(answer.verify_value([4, 5, 6]))  # Different lists
        self.assertEqual(
            answer.message_content,
            'Expected [1, 2, 3], but received [4, 5, 6].'
        )

    def test_verify_value_string_vs_non_string(self):
        # Test when one is a string and the other is not
        answer = Answer(expected="42")
        self.assertFalse(answer.verify_value(42))
        self.assertEqual(
            answer.message_content,
            'Expected "42", but received 42.'
        )

    def test_verify_value_non_string_vs_string(self):
        answer = Answer(expected=42)
        self.assertFalse(answer.verify_value("42"))
        self.assertEqual(
            answer.message_content,
            'Expected 42, but received "42".'
        )

    #
    # test_verify method
    #

    def test_verify_strict_mode_type_and_value_match(self):
        # Test strict mode with matching type and value
        answer = Answer(expected=42, strict=True)
        self.assertTrue(answer.verify(42))  # Both type and value match

    def test_verify_strict_mode_type_mismatch(self):
        # Test strict mode with type mismatch
        answer = Answer(expected=42, strict=True)
        self.assertFalse(answer.verify("42"))  # Type mismatch
        self.assertEqual(
            answer.message_content,
            'Expected object of type <class \'int\'>, but received <class \'str\'> 42.'
        )

    def test_verify_strict_mode_value_mismatch(self):
        # Test strict mode with matching type but different value
        answer = Answer(expected=42, strict=True)
        self.assertFalse(answer.verify(100))  # Value mismatch
        self.assertEqual(
            answer.message_content,
            'Expected 42, but received 100.'
        )

    def test_verify_non_strict_mode_type_mismatch(self):
        # Test non-strict mode with type mismatch
        answer = Answer(expected=42, strict=False)
        self.assertFalse(answer.verify("42"))  # Type mismatch but should only care about value
        self.assertEqual(
            answer.message_content,
            'Expected 42, but received "42".'
        )

    def test_verify_non_strict_mode_value_match(self):
        # Test non-strict mode with value match
        answer = Answer(expected=42, strict=False)
        self.assertTrue(answer.verify(42))  # Value match

    def test_verify_non_strict_mode_value_mismatch(self):
        # Test non-strict mode with value mismatch
        answer = Answer(expected=42, strict=False)
        self.assertFalse(answer.verify(100))  # Value mismatch
        self.assertEqual(
            answer.message_content,
            'Expected 42, but received 100.'
        )

    #
    # test value_to_literal method

    def test_value_to_literal_with_string(self):
        # Test when the input is a string
        result = Answer.value_to_literal("test")
        self.assertEqual(result, "'test'")

        result = Answer.value_to_literal("another string")
        self.assertEqual(result, "'another string'")

    def test_value_to_literal_with_non_string(self):
        # Test when the input is not a string
        result = Answer.value_to_literal(42)
        self.assertEqual(result, 42)

        result = Answer.value_to_literal(3.14)
        self.assertEqual(result, 3.14)

        result = Answer.value_to_literal([1, 2, 3])
        self.assertEqual(result, [1, 2, 3])

        result = Answer.value_to_literal({'key': 'value'})
        self.assertEqual(result, {'key': 'value'})

    def test_value_to_literal_with_empty_string(self):
        # Test when the input is an empty string
        result = Answer.value_to_literal("")
        self.assertEqual(result, "''")


if __name__ == '__main__':
    unittest.main()