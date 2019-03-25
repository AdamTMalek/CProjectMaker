import unittest
from contextlib import contextmanager
from io import StringIO
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

    def test_verbosity_condition(self):
        """
        Test if the message is printed or not depending on minimum level of verbosity
        :return:
        """

        # We use captured_output to capture the output of a function to stdout or stderr
        @contextmanager
        def captured_output():
            out, err = StringIO(), StringIO()
            old_out, old_err = sys.stdout, sys.stderr
            try:
                sys.stdout, sys.stderr = out, err
                yield sys.stdout
            finally:
                sys.stdout, sys.stderr = old_out, old_err

        verbosity = 3
        verbose = Verbose(verbosity)

        # Testing function
        def test(min_level, output_expected):
            with self.subTest(set=verbosity, min=min_level):
                with captured_output() as output:
                    verbose.print(MessageType.INFO, "foo", min_level, stream=output)
                    message_printed = output.getvalue() != ""
                    self.assertEqual(output_expected, message_printed)

        # Test expected no output:
        test(4, output_expected=False)
        # Test expected some output
        test(3, output_expected=True)
        test(2, output_expected=True)
