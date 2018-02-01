import unittest
import tests.loader as loader

cpm = loader.load("cpm")


class TestMain(unittest.TestCase):
    """
    Test the cpm module
    """

    def test_no_project_name(self):
        """
        Test if the main function accepts no project name to be given.
        We expect it to return False because the name is required
        """
        args = {"cpm"}  # The first argument is the filename we run
        self.assertFalse(cpm.main(args))

    def test_invalid_name(self):
        """
        We expect the method to only accept alphabetic characters.
        Test with some numbers, special characters to check if the function accepts the input
        """
        invalid_names = {"hello world", "53project", "!project", "\"project\""}
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(cpm.valid_name(name))

    def test_valid_name(self):
        """
        Test if name validator accepts valid name
        """
        name = "HelloWorld"
        self.assertTrue(cpm.valid_name(name))