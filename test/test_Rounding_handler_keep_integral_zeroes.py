from src.precise_value import (Precise_value, Rounding_handler,
        Rounding_handler_keep_integral_zeroes, Rounding_handler_proper)
import unittest

class test_Rounding_handler_keep_integral_zeroes(unittest.TestCase):
    def setUp(self):
        self.rounding_handler = Rounding_handler_keep_integral_zeroes

    def test_repr(self):
        rh = self.rounding_handler
        a = Precise_value('34', rh)
        self.assertEqual(a.__str__(), '34')

    
