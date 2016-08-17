from src.precise_value import Precise_value
import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.value_1 = Precise_value('no_rounding', '3')
        self.assertEqual(self.value_1, Precise_value('no_rounding', '3'))
        self.value_2 = Precise_value('no_rounding', '2')

    def test_add(self):
        self.assertEqual(self.value_1 + self.value_2, Precise_value('no_rounding', '5'))

    def test_arithemtic_only_if_same_rounding_methods(self):
        nothing=None
