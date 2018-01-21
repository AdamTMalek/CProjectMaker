import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import tests.loader as loader

cpm = loader.load("cpm")


class TestMain(unittest.TestCase):
    """
    Test the cpm module
    """

    @contextmanager
    def captured_output(self):
        """
        Captures standard output and standard error
        """
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr

        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

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
                with self.captured_output():  # Use captured_output to silence any error messages
                    self.assertFalse(cpm.valid_name(name))

    def test_valid_name(self):
        """
        Test if name validator accepts valid name
        """
        name = "HelloWorld"
        self.assertTrue(cpm.valid_name(name))