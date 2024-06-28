# coding: utf-8
import doctest
import unittest

import python_package as pkg


class TestDoctests(unittest.TestCase):
    def run_doctest(self, module):
        report = doctest.testmod(module)
        self.assertFalse(report.failed)

    def test_modules(self):
        self.run_doctest(pkg)
