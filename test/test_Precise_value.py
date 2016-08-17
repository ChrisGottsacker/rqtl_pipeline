from src.precise_value import (Precise_value, Rounding_handler,
        Rounding_handler_keep_integral_zeroes, Rounding_handler_proper)
import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.value_1 = Precise_value(Rounding_handler, '3')
        self.assertEqual(self.value_1, Precise_value(Rounding_handler, '3'))
        self.value_2 = Precise_value(Rounding_handler, '2')

    def test_add(self):
        self.assertEqual(self.value_1 + self.value_2, Precise_value(Rounding_handler, '5'))

    def test_arithemtic_only_if_same_rounding_methods(self):
        nothing=None
