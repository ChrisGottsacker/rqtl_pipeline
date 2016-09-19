from src.precise_value import (Precise_value, Rounding_handler,
        Rounding_handler_keep_integral_zeroes, Rounding_handler_proper)
import unittest

pv = Precise_value

class test_Rounding_handler_keep_integral_zeroes(unittest.TestCase):
    def setUp(self):
        self.value_1 = pv('3', Rounding_handler)
        self.assertEqual(self.value_1, pv('3', Rounding_handler))
        self.value_2 = pv('2', Rounding_handler)
        self.rounding_handler = Rounding_handler

    def test_init(self):
        a = pv('3.34', Rounding_handler)
        self.assertEqual(str(a.fixed_point_value_unrounded), '3.34')
        # self.assertEqual(str(a.num_all_significant_digits), '3')
        # self.assertEqual(str(a.num_significant_decimal_digits), '2')

    def test_intermediate(self):
        a = pv.intermediate('3.34', Rounding_handler, 3, 2)
        self.assertEqual(str(a.fixed_point_value_unrounded), '3.34')
        self.assertEqual(str(a.num_all_significant_digits), '3')
        self.assertEqual(str(a.num_significant_decimal_digits), '2')

    def  notreadyto_test_str(self):
        a = pv('1.3E4', Rounding_handler)
        self.assertEqual(a.__str__(), '1.3E4')

    def notreadyto_test_add(self):
        rh = self.rounding_handler

        a = pv('23', rh)
        b = pv('13', rh)
        self.assertTrue(type(a), type(a + b))

        # Show that no rounding happens
        self.assertEqual(pv('1', rh) + pv('1.0', rh), pv('2.0', rh))
        'TODO: add more tests'

    def test_arithemtic_only_if_same_rounding_methods(self):
        nothing=None
