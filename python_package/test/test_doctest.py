"""Tests for docstring tests."""

import doctest
import unittest

import python_package as pkg


class TestDoctests(unittest.TestCase):
    def _run_doctest(self, module):
        report = doctest.testmod(module)
        self.assertFalse(report.failed)

    def test_modules(self):
        """Run doctests in modules."""
        self._run_doctest(pkg)
