import unittest
import tests.loader as loader

cpm = loader.load("cpm")


class TestMain(unittest.TestCase):
    """
    Test the cpm module
    """

    def test_invalid_name(self):
        """
        We expect the method to only accept alphabetic characters.
        Test with some numbers, special characters to check if the function accepts the input
        """
        invalid_names = {"hello world", "!project", "\"project\""}
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(cpm.valid_name(name))

    def test_valid_name(self):
        """
        Test if name validator accepts valid name
        """
        valid_names = {"helloworld", "project1", "12project", "3301", "1project1"}
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(cpm.valid_name(name))

