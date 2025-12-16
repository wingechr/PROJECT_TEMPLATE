"""Example unit tests."""

import unittest

from python_package import get_info


class TestTemplate(unittest.TestCase):
    def setUp(self):
        """Set up for each method."""

    def tearDown(self):
        """Tear down for each method."""

    @classmethod
    def setUpClass(cls):
        """Set up once for all methods in class."""

    @classmethod
    def tearDownClass(cls):
        """Tear down once for all methods in class."""

    def test_get_info(self):
        """Test get_info() function."""
        result = get_info()
        self.assertEqual(set(result), {"version", "python", "platform"})
