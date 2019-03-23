import unittest
from project.module import match_and_replace_include as replace_include

class ModuleTest(unittest.TestCase):
    """
    Provides tests for the module.py script
    """

    def test_include_regex(self):
        """
        Test the include regex used to find and replace #include... when renaming the module
        :return:
        """
        tests = [
            {
                'original': '#include "foo.h"',
                'expected': '#include "bar.h"',
            },
            {
                'original': '#include "foo/foo.h"',
                'expected': '#include "bar/bar.h"',
            },
            {
                'original': '#include "../foo/foo.h"',
                'expected': '#include "../bar/bar.h"',
            },
            {
                'original': '#include "../xyz/foo.h"',
                'expected': '#include "../xyz/bar.h"',
            },
            {
                'original': '#include "../xyz/foo/foo.h"',
                'expected': '#include "../xyz/bar/bar.h"',
            },
        ]

        for test in tests:
            with self.subTest(original=test['original']):
                self.assertEqual(test['expected'], replace_include(test['original'], 'foo', 'bar'))
