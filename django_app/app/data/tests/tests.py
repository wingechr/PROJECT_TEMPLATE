from data.models import Data
from django.test import TestCase


class TestUnmanagedTableFail(TestCase):
    # how does the unmanaged database table
    # for Data behave in test?

    # databases = {"default", "data"}

    def test_unmanaged_table_fail(self):
        # normal query of data should fail:
        self.assertRaises(Exception, Data.objects.count)
