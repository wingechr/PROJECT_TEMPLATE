# coding: utf-8
import unittest

from python_package import get_info


class TestTemplate(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_info(self):
        result = get_info()
        self.assertEqual(set(result), {"version", "python", "platform"})
