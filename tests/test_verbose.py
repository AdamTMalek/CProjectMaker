import unittest
from scripts.verbose import *


class VerboseTest(unittest.TestCase):
    def test_initialisation(self):
        """
        Test if the Verbose constructor will throw an error with incorrect types of verbosity_level argument
        """
        def test(verbosity, error_expected=True):
            with self.subTest(type=verbosity):
                error_thrown = False
                try:
                    Verbose(verbosity)
                except TypeError:
                    error_thrown = True
                self.assertEqual(error_expected, error_thrown)

        # Test with incorrect types:
        test("foo")
        test(53.2)
        # Test with correct type:
        test(-1, error_expected=False)
        test(3, error_expected=False)

    def test_message_type(self):
        """
        Test if an invalid message type raises a TypeError exception
        """
        def test(message_type, error_expected=True):
            with self.subTest(type=message_type):
                error_thrown = False
                try:
                    verbose.print(message_type, "foo", stream=sys.stdout)
                except TypeError:
                    error_thrown = True
                self.assertEqual(error_expected, error_thrown)

        # Create an object of Verbose
        verbose = Verbose(verbosity_level=0)  # Verbosity level does not matter
        # Test with incorrect types:
        test(0)
        test("foo")
        test(MessageType)
        # Test with correct types:
        print("--- ignore ---")
        test(MessageType.INFO, error_expected=False)
        test(MessageType.WARNING, error_expected=False)
        test(MessageType.ERROR, error_expected=False)
        print("--------------")

    def test_print_level(self):
        """
        Test if the print function will throw an error with incorrect types of min_level argument
        """
        verbose = Verbose(5)

        def test(level, error_expected=True):
            with self.subTest(type=level):
                error_thrown = False
                try:
                    verbose.print(MessageType.INFO, "foo", level, stream=sys.stdout)
                except TypeError:
                    error_thrown = True
                self.assertEqual(error_expected, error_thrown)

        # Test with incorrect types:
        test("foo")
        test(53.2)
        # Test with correct type:
        print("--- ignore ---")
        test(-1, error_expected=False)
        test(3, error_expected=False)
        print("--------------")

    def test_print_stream(self):
        """
        Test if the print function will throw an error with incorrect stream
        """
        verbose = Verbose(5)

        def test(stream, error_expected=True):
            with self.subTest(type=stream):
                error_thrown = False
                try:
                    verbose.print(MessageType.INFO, "foo", stream=stream)
                except ValueError:
                    error_thrown = True
                self.assertEqual(error_expected, error_thrown)

        print("--- ignore ---")
        # Test incorrect:
        test("foo")
        test(sys.stdin)
        # Test correct:
        test(sys.stdout, error_expected=False)
        test(sys.stderr, error_expected=False)
        print("--------------")
