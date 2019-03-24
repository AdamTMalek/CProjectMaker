import unittest
from scripts.module import rename_in_include as replace_include
from scripts.module import rename_header_constant as replace_header


class ModuleTest(unittest.TestCase):
    """
    Provides tests for the module.py script
    """

    def test_include_regex(self):
        """
        Test the include regex used to find and replace #include... when renaming the module
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
                self.assertEqual(test['expected'], replace_include(test['original'], 'foo', 'bar')[0])

    def test_header_regex(self):
        """
        Test the header regex used to find and replace include-guard-constants inside a header
        """
        tests = [
            {
                'original': '#ifndef FOO_H',
                'expected': '#ifndef BAR_H'
            },
            {
                'original': '#define FOO_H',
                'expected': '#define BAR_H'
            },
            {
                'original': '#endif /* FOO_H */',
                'expected': '#endif /* BAR_H */',
            },
            {
                'original': '// Lorem ipsum FOO_H dolor sit amet',
                'expected': '// Lorem ipsum BAR_H dolor sit amet'
            },
        ]

        for test in tests:
            with self.subTest(original=test['original']):
                self.assertEqual(test['expected'], replace_header(test['original'], 'foo', 'bar'))
