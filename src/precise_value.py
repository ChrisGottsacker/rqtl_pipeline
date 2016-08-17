from abc import ABCMeta, abstractmethod
from decimal import Decimal
from enum import Enum
import re
import sys

class Precise_value(object):
    def __init__(self, rounding_method, value):
        '''value can be any type that Decimal() accepts'''
        self.fixed_point_value = Decimal(value)
        self.string_value = str(value)
        self.set_rounding_handler(rounding_method)
        self.update_significant_digit_counts()

    def set_rounding_handler(self, rounding_method):
        if rounding_method == 'no_rounding':
            self.rounding_handler = Rounding_handler
        elif rounding_method == 'keep_integral_zeroes':
            self.rounding_handler = Rounding_handler_keep_integral_zeroes
        elif rounding_method == 'proper':
            self.rounding_handler = Rounding_handler_proper
        else:
            sys.exit('Error: rounding_method "' + rounding_method + '" does not exist.')

    '''Arithmetic Operators:'''
    def __add__(self, other):
        if self.can_do_arithmetic(other):
            return( self.rounding_handler.add(self, other) )

    def __sub__(self, other):
        if self.can_do_arithmetic(other):
            return( self.rounding_handler.sub(self, other) )

    def __mul__(self, other):
        if self.can_do_arithmetic(other):
            return( self.rounding_handler.mul(self, other) )

    def __div__(self, other):
        if self.can_do_arithmetic(other):
            return( self.rounding_handler.div(self, other) )

    '''Comparison Operators:'''
    '''TODO: consider error-checking'''
    def __lt__(self, other):
        return( self.fixed_point_value < other.fixed_point_value )

    def __le__(self, other):
        return( self.fixed_point_value <= other.fixed_point_value )

    def __eq__(self, other):
        return( self.fixed_point_value == other.fixed_point_value )

    def __ne__(self, other):
        return( self.fixed_point_value != other.fixed_point_value )

    def __ge__(self, other):
        return( self.fixed_point_value >= other.fixed_point_value )

    def __gt__(self, other):
        return( self.fixed_point_value > other.fixed_point_value )

    def can_do_arithmetic(self, other):
        '''TODO raise exception or quit if math can't be done'''
        return( Precise_value.is_precise_value_object(other) and self.are_rounding_handlers_same(other) )

    @classmethod
    def is_precise_value_object(cls, value):
        return(isinstance(value, cls))

    def are_rounding_handlers_same(self, other):
        return(self.rounding_handler.__class__ is other.rounding_handler.__class__)

    def update_significant_digit_counts(self):
        self.num_significant_digits = self.rounding_handler.num_significant_digits(self.string_value)
        self.num_significant_decimal_digits = self.rounding_handler.num_significant_decimal_digits(self.string_value)


class Rounding_handler(metaclass=ABCMeta):
    '''Base class for rounding handlers. Does NO rounding.'''
    @classmethod
    def add(cls, operand_1, operand_2):
        fixed_point_value = operand_1.fixed_point_value + operand_2.fixed_point_value
        rounded_fixed_point_value = cls.round_decimal_digits(
            fixed_point_value, operand_1, operand_2)
        return( Precise_value(operand_1.rounding_method, rounded_fixed_point_value) )

    def sub(operand_1, operand_2):
        return( operand_1.fixed_point_value - operand_2.fixed_point_value )

    def mul(operand_1, operand_2):
        return( operand_1.fixed_point_value * operand_2.fixed_point_value )

    def div(operand_1, operand_2):
        return( operand_1.fixed_point_value / operand_2.fixed_point_value )

    @abstractmethod
    def round_decimal_digits(calculated_value, operand_1, operand_2):
        return( calculated_value )
        
    @abstractmethod
    def num_significant_decimal_digits(value):
        '''Counts number of significant digits to right of decimal point'''
        return(None)

    @abstractmethod
    def num_significant_digits(value):
        '''Counts number of significant figures in a numeric string.'''
        return(None)

    @abstractmethod
    def get_significant_digits(value):
        return(None)

    @abstractmethod
    def get_significant_decimal_digits(value):
        return(None)

    def remove_decimal_point(value):
        return( re.sub(r'\.', r'', value) )

    def remove_non_digits(value):
        '''Remove scientific notation characters and negation sign
        	-03.05E+4 -> 03.05'''
        return( re.sub(r'^-*((\d+\.?\d*)|(\d*\.\d+)).*$', r'\1', value) )

    def remove_leading_zeroes(value):
        '''Remove leading zeroes to left of decimal point, keeping at most 1 zero
        e.g. -03.05E+4 -> 305E+4    or    05 -> 5    or   0.4 -> .4    or   00 -> 0'''
        return( re.sub(r'^0*(\d\.?\d*)$', r'\1', value) )

    def remove_decimal_placeholding_zeroes(value):
        '''Remove leading zeroes to right of decimal point, plus any immediately to
        the left of decimal point, if value < 1
        e.g. .05 -> .5    or   0.01 -> .1'''
        return( re.sub(r'^0*(\.)0*(\d+)$', r'\1\2', value) )

    def remove_integral_placeholding_zeroes(value):
        '''Remove trailing zeroes to right of integer w/ no decimal point
        e.g. 100 -> 1   but   100. -> 100.'''
        return( re.sub(r'^([1-9]+)0*$', r'\1', value) )


class Rounding_handler_keep_integral_zeroes(Rounding_handler, metaclass=ABCMeta):
    def round_decimal_digits(calculated_value, operand_1, operand_2):
        num_digits_to_keep = min(operand_1.num_significant_decimal_digits, operand_2.num_significant_decimal_digits)
        return( calculated_value.quantize(Decimal(str(pow(10,-num_digits_to_keep))),
        rounding=ROUND_HALF_EVEN) )

    def num_significant_digits(value):
        '''Counts number of significant figures in a numeric string.'''
        parsed_value = Rounding_handler_keep_integral_zeroes.get_significant_digits(value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_decimal_point(parsed_value) # remove decimal point
        return( len( parsed_value ) )

    def num_significant_decimal_digits(value):
        '''Counts number of significant digits to right of decimal point'''
        return( len(get_significant_decimal_digits(value)) )

    def get_significant_digits(value):
        '''Remove non digits, undesired zeroes, scientific notation characters,
        but leave the decimal point.
            e.g. -034.5E+3 -> 34.5    or   0.004 -> .4'''
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_non_digits(value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_leading_zeroes(parsed_value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_decimal_placeholding_zeroes(parsed_value)
        return( parsed_value )

    def get_significant_decimal_digits(value):
        parsed_value = remove_non_digits(value)
        parsed_value = remove_decimal_placeholding_zeroes(parsed_value)
        return( parsed_value.split('.')[1] )



class Rounding_handler_proper(Rounding_handler_keep_integral_zeroes):
    def get_significant_digits(value):
        parsed_value = super().get_significant_digits(value)
        parsed_value = Rounding_handler_proper.remove_integral_placeholding_zeroes(parsed_value)
        return( parsed_value )
