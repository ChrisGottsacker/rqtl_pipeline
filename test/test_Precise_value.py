from src.precise_value import (Precise_value, Rounding_handler,
        Rounding_handler_keep_integral_zeroes, Rounding_handler_proper)
import unittest

class test_Rounding_handler_keep_integral_zeroes(unittest.TestCase):
    def setUp(self):
        self.value_1 = Precise_value(Rounding_handler, '3')
        self.assertEqual(self.value_1, Precise_value(Rounding_handler, '3'))
        self.value_2 = Precise_value(Rounding_handler, '2')
        self.rounding_handler = Rounding

    def test_add(self):
        rh = self.rounding_handler
        a = pv('23', rh)
        b = pv('13', rh)
        self.assertTrue(type(a), type(a + b))

        # Show that no rounding happens
        self.assertEqual(pv('1', rh) + pv('1.0', rh), pv('2.0', rh))
        'TODO: add more tests'

    def test_arithemtic_only_if_same_rounding_methods(self):
        nothing=None
