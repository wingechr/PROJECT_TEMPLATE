from data.models import Data
from django.test import TestCase
from django.test.testcases import DatabaseOperationForbidden


class TestUnmanagedTableFail(TestCase):
    # how does the unmanaged database table
    # for Data behave in test?

    databases = {"default", "data"}

    def test_unmanaged_table_fail(self):
        # normal query of data should fail:
        self.assertRaises(DatabaseOperationForbidden, Data.objects.count)
