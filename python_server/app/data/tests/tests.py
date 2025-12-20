"""Unit tests."""

from data.models import Data
from django.test import TestCase


class TestUnmanagedTableFail(TestCase):
    """how does the unmanaged database table for Data behave in test?"""

    def test_unmanaged_table_fail(self):
        """Normal query of data should fail"""
        self.assertRaises(Exception, Data.objects.count)
