from src.precise_value import (Precise_value, Rounding_handler,
        Rounding_handler_keep_integral_zeroes, Rounding_handler_proper)
import unittest

class test_Rounding_handler(unittest.TestCase):

    def setUp(self):
        self.rounding_handler = Rounding_handler

    def test_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Rounding_handler()

    def test_remove_decimal_point(self):
        rdp = self.rounding_handler.remove_decimal_point

        # test if decimal point removed if string contains one
        self.assertEqual(rdp('.'), '')
        self.assertEqual(rdp('1.'), '1')
        self.assertEqual(rdp('.1'), '1')
        self.assertEqual(rdp('-.1'), '-1')
        self.assertEqual(rdp('-1.2E3'), '-12E3')

        # test if string unchanged if string doesn't contain a decimal point
        self.assertEqual(rdp('1248'), '1248')
        self.assertEqual(rdp('1200'), '1200')
        self.assertEqual(rdp('1'), '1')
        self.assertEqual(rdp('01'), '01')
        self.assertEqual(rdp('1E3'), '1E3')

    def test_remove_non_digits(self):
        rnd = Rounding_handler.remove_non_digits

        # test if negation sign and scientific notation are removed
        self.assertEqual(rnd('-.1'), '.1')
        self.assertEqual(rnd('-1.1'), '1.1')
        self.assertEqual(rnd('-1'), '1')
        self.assertEqual(rnd('-10'), '10')
        self.assertEqual(rnd('-1.2E3'), '1.2')
        self.assertEqual(rnd('1.2E3'), '1.2')

        # test if $ sign is removed
        self.assertEqual(rnd('$-.1'), '.1')
        self.assertEqual(rnd('$-1.1'), '1.1')
        self.assertEqual(rnd('$-1'), '1')
        self.assertEqual(rnd('$-10'), '10')
        self.assertEqual(rnd('$-1.2E3'), '1.2')
        self.assertEqual(rnd('$.1'), '.1')
        self.assertEqual(rnd('$1.1'), '1.1')
        self.assertEqual(rnd('$1'), '1')
        self.assertEqual(rnd('$10'), '10')
        self.assertEqual(rnd('$1.2E3'), '1.2')

        # test if % sign is removed
        self.assertEqual(rnd('-.1%'), '.1')
        self.assertEqual(rnd('-1.1%'), '1.1')
        self.assertEqual(rnd('-1%'), '1')
        self.assertEqual(rnd('-10%'), '10')
        self.assertEqual(rnd('-1.2E3%'), '1.2')
        self.assertEqual(rnd('.1%'), '.1')
        self.assertEqual(rnd('1.1%'), '1.1')
        self.assertEqual(rnd('1%'), '1')
        self.assertEqual(rnd('10%'), '10')
        self.assertEqual(rnd('1.2E3%'), '1.2')

        # test if anything is removed which shouldn't be
        self.assertEqual(rnd('1'), '1')
        self.assertEqual(rnd('11'), '11')
        self.assertEqual(rnd('1.1'), '1.1')
        self.assertEqual(rnd('.1'), '.1')
        self.assertEqual(rnd('10'), '10')
        self.assertEqual(rnd('1.0'), '1.0')
        self.assertEqual(rnd('0.1'), '0.1')

    def test_remove_leading_zeroes(self):
        rlz = Rounding_handler.remove_leading_zeroes

        # test if leading integral zeros are removed
        self.assertEqual(rlz('0.0'), '0.0')
        self.assertEqual(rlz('00'), '0')
        self.assertEqual(rlz('-0.1'), '-.1')
        self.assertEqual(rlz('-01.1'), '-1.1')
        self.assertEqual(rlz('-001'), '-1')
        self.assertEqual(rlz('-010'), '-10')
        self.assertEqual(rlz('-01.2E3'), '-1.2E3')
        self.assertEqual(rlz('0.1'), '.1')
        self.assertEqual(rlz('01.1'), '1.1')
        self.assertEqual(rlz('01'), '1')
        self.assertEqual(rlz('010'), '10')
        self.assertEqual(rlz('01.2E3'), '1.2E3')

        # test if anything removed that shouldn't be
        self.assertEqual(rlz('0.0'), '0.0')
        self.assertEqual(rlz('0'), '0')
        self.assertEqual(rlz('-0.1'), '-.1')
        self.assertEqual(rlz('-1.1'), '-1.1')
        self.assertEqual(rlz('-1'), '-1')
        self.assertEqual(rlz('-10'), '-10')
        self.assertEqual(rlz('-1.2E3'), '-1.2E3')
        self.assertEqual(rlz('0.1'), '.1')
        self.assertEqual(rlz('1.1'), '1.1')
        self.assertEqual(rlz('1'), '1')
        self.assertEqual(rlz('10'), '10')
        self.assertEqual(rlz('11'), '11')
        self.assertEqual(rlz('1.2E3'), '1.2E3')

    def test_remove_decimal_placeholding_zeroes(self):
        rdpz= Rounding_handler.remove_decimal_placeholding_zeroes

        # test if zeroes removed
        self.assertEqual(rdpz('0.0'), '0.')
        self.assertEqual(rdpz('0.00'), '0.')
        self.assertEqual(rdpz('.00'), '.0')
        self.assertEqual(rdpz('.03'), '.3')
        self.assertEqual(rdpz('0.03'), '0.3')
        self.assertEqual(rdpz('-0.0'), '-0.')
        self.assertEqual(rdpz('-0.00'), '-0.')
        self.assertEqual(rdpz('-.00'), '-.0')
        self.assertEqual(rdpz('-.03'), '-.3')
        self.assertEqual(rdpz('-0.03'), '-0.3')

        # test if anything removed that shouldn't be
        self.assertEqual(rdpz('0'), '0')
        self.assertEqual(rdpz('-0.1'), '-0.1')
        self.assertEqual(rdpz('-1.1'), '-1.1')
        self.assertEqual(rdpz('-1'), '-1')
        self.assertEqual(rdpz('-10'), '-10')
        self.assertEqual(rdpz('-1.2E3'), '-1.2E3')
        self.assertEqual(rdpz('0.1'), '0.1')
        self.assertEqual(rdpz('1.1'), '1.1')
        self.assertEqual(rdpz('1'), '1')
        self.assertEqual(rdpz('10'), '10')
        self.assertEqual(rdpz('11'), '11')
        self.assertEqual(rdpz('1.2E3'), '1.2E3')

    def test_remove_integral_placeholding_zeroes(self):
        ripz = Rounding_handler.remove_integral_placeholding_zeroes

        # test if zeroes removed
        self.assertEqual(ripz('-10'), '-1')
        self.assertEqual(ripz('10'), '1')
        self.assertEqual(ripz('10.'), '10.')
        self.assertEqual(ripz('10.E4'), '10.E4')
        self.assertEqual(ripz('10E4'), '1E4')

        # test if anything removed that shouldn't be
        self.assertEqual(ripz('0'), '0')
        self.assertEqual(ripz('-0.1'), '-0.1')
        self.assertEqual(ripz('-1.1'), '-1.1')
        self.assertEqual(ripz('-1'), '-1')
        self.assertEqual(ripz('-1.2E3'), '-1.2E3')
        self.assertEqual(ripz('0.1'), '0.1')
        self.assertEqual(ripz('1.1'), '1.1')
        self.assertEqual(ripz('1'), '1')
        self.assertEqual(ripz('11'), '11')
        self.assertEqual(ripz('1.2E3'), '1.2E3')
