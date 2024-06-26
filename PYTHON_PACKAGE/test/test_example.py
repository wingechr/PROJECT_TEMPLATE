# coding: utf-8
import unittest


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

    # EXAMPLE
    def test_TEMPLATE(self):
        self.assertEqual(True, True, "Warning message")
