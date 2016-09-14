from abc import ABCMeta, abstractmethod
from decimal import Decimal
from enum import Enum
import re
import sys

class Precise_value(object):
    '''
    A numeric type that obeys significant figure arithmetic rules.

    Wrapper for Decimal object.
    '''

    def __init__(self, value, rounding_handler):
        '''
        Constructs new Precise Value, assumes value is rounded to correct precision.

        Keyword arguments:
        value -- can be any type that Decimal accepts
        rounding_method -- reference to one of the Rounding Handler classes
        '''
        # Use for intermediate arithmetic. Never rounded. Not correct precision.
        self.fixed_point_value_unrounded = Decimal(value)
        # Use for comparisons, display purposes. (Rouneded to) Correct precision
        self.fixed_point_value_rounded = self.fixed_point_value_unrounded
        # Specifies how rounding should be done
        self.rounding_handler = rounding_handler

        # Counts how many digits are significant
        value_as_string = self.__str__()
        self.num_all_significant_digits = +\
            self.rounding_handler.num_all_significant_digits(value_as_string)
        self.num_significant_decimal_digits = +\
            self.rounding_handler.num_significant_decimal_digits(value_as_string)



    def __init__(self, value, rounding_handler, num_all_significant_digits,
                    num_significant_decimal_digits):
        '''
        Constructs new Precise Value, assumes value may not have correct precision.

        This constructor is typically used to make Precise Values that are part
        of an intermediate calculation. The num_all_significant_digits and
        num_significant_decimal_digits parameters enable rounding value to
        its correct precision (according to rules specified by rounding_handler).

        Keyword arguments:
        value -- can be any type that Decimal accepts
        rounding_method -- reference to one of the Rounding Handler classes
        num_all_significant_digits -- quantity used to know how to round
        num_significant_decimal_digits -- quantity used to know how to round
        '''
        # Use for intermediate arithmetic. Never rounded. Not correct precision.
        self.fixed_point_value_unrounded = Decimal(value)
        # Use for comparisons, display purposes. (Rouneded to) Correct precision.
        # Kept current by all functions, so its value is always accurate.
        self.fixed_point_value_rounded = rounding_handler.round(self)
        # Specifies how rounding should be done
        self.rounding_handler = rounding_handler

        self.num_all_significant_digits = num_all_significant_digits
        self.num_significant_decimal_digits = num_significant_decimal_digits

    def __str__(self):
        return( str(self.fixed_point_value_rounded) )

    '''Arithmetic Operators:'''
    # Any operation that changes this Precise Value's value must update
    # self.fixed_point_value_rounded
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
        return( self.fixed_point_value_rounded < other.fixed_point_value_rounded )

    def __le__(self, other):
        return( self.fixed_point_value_rounded <= other.fixed_point_value_rounded )

    def __eq__(self, other):
        return( self.fixed_point_value_rounded == other.fixed_point_value_rounded )

    def __ne__(self, other):
        return( self.fixed_point_value_rounded != other.fixed_point_value_rounded )

    def __ge__(self, other):
        return( self.fixed_point_value_rounded >= other.fixed_point_value_rounded )

    def __gt__(self, other):
        return( self.fixed_point_value_rounded > other.fixed_point_value_rounded )

    def can_do_arithmetic(self, other):
        '''TODO raise exception or quit if math can't be done'''
        return( Precise_value.is_precise_value_object(other) and self.are_rounding_handlers_same(other) )

    @classmethod
    def is_precise_value_object(cls, value):
        return(isinstance(value, cls))

    def are_rounding_handlers_same(self, other):
        return(self.rounding_handler.__class__ is other.rounding_handler.__class__)



class Rounding_handler(metaclass=ABCMeta):
    '''
    Simple Rounding Handler, does NO rounding. Significant figures are irrelevant.
    Use class inherited from this one to do actual rounding.
    '''
    @classmethod
    def add(cls, operand_1, operand_2):
        # Do arithmetic using wrapped class's magic functions
        fixed_point_value = operand_1.fixed_point_value + operand_2.fixed_point_value
        rounded_fixed_point_value = cls.round_decimal_digits(
            fixed_point_value, operand_1, operand_2)
        return( Precise_value(rounded_fixed_point_value, operand_1.rounding_handler) )

    @classmethod
    def sub(cls, operand_1, operand_2):
        # Do arithmetic using wrapped class's magic functions
        fixed_point_value = operand_1.fixed_point_value - operand_2.fixed_point_value
        rounded_fixed_point_value = cls.round_decimal_digits(
            fixed_point_value, operand_1, operand_2)
        return( Precise_value(rounded_fixed_point_value, operand_1.rounding_handler) )

    @classmethod
    def mul(cls, operand_1, operand_2):
        # Do arithmetic using wrapped class's magic functions
        fixed_point_value = operand_1.fixed_point_value * operand_2.fixed_point_value
        rounded_fixed_point_value = cls.round_all_significant_digits(
            fixed_point_value, operand_1, operand_2 )
        return( Precise_value(rounded_fixed_point_value, operand_1.rounding_handler) )

    @classmethod
    def div(cls, operand_1, operand_2):
        # Do arithmetic using wrapped class's magic functions
        fixed_point_value = operand_1.fixed_point_value / operand_2.fixed_point_value
        rounded_fixed_point_value = cls.round_all_significant_digits(
            fixed_point_value, operand_1, operand_2 )
        return( Precise_value(rounded_fixed_point_value, operand_1.rounding_handler) )

    @abstractmethod
    def round_decimal_digits(calculated_value, operand_1, operand_2):
        return( calculated_value )

    @abstractmethod
    def round_all_significant_digits(calculated_value, operand_1, operand_2):
        return(calculated_value)

    @abstractmethod
    def num_significant_decimal_digits(value):
        '''Counts number of significant digits to right of decimal point'''
        return(None)

    @abstractmethod
    def num_all_significant_digits(value):
        '''Counts total number of significant figures in a numeric string.'''
        return(None)

    @abstractmethod
    def get_all_significant_digits(value):
        return(None)

    @abstractmethod
    def get_significant_decimal_digits(value):
        return(None)

    def remove_decimal_point(value):
        return( re.sub(r'\.', r'', value) )

    def remove_non_digits(value):
        '''Remove scientific notation characters, negation sign, dollar sign
        	-03.05E+4 -> 03.05'''
        return( re.sub(r'^(-|\$)*((\d+\.?\d*)|(\d*\.\d+)).*$', r'\2', value) )

    def remove_leading_zeroes(value):
        '''Remove leading zeroes to left of decimal point, keeping at most 1 zero
        e.g. -03.05E+4 -> -3.05E+4    or    05 -> 5    or   0.4 -> .4    or   00 -> 0'''
        return( re.sub(r'^(-|\$)*0*(([1-9]+.*)|(\.0*[1-9]+.*)|(\d.*))$', r'\1\2', value) )

    def remove_decimal_placeholding_zeroes(value):
        '''Remove leading zeroes to right of decimal point, plus any immediately to
        the left of decimal point, if value < 1
        e.g. .05 -> .5    or   0.01 -> .1   but   0 -> 0 and .0 -> .0'''
        # if no digits on left, keep up to one placeholding zero on right
        temp = re.sub(r'^(-|\$)*(\.)0*(\d+)(.*)$', r'\1\2\3\4', value)
        # if at least one digit on left, remove all placeholding zeroes on right
        temp = re.sub(r'^(-|\$)*(0+\.)0*(\d*)(.*)$', r'\1\2\3\4', temp)
        return( temp )

    def remove_integral_placeholding_zeroes(value):
        '''Remove trailing zeroes to right of integer w/ no decimal point
        e.g. 100 -> 1   but   100. -> 100.'''
        return( re.sub(r'^(-|\$)*([1-9]+)0*(?!\.)(.*)$', r'\1\2\3', value) )


class Rounding_handler_keep_integral_zeroes(Rounding_handler, metaclass=ABCMeta):
    '''
    100     has 3 sigfigs
    10.0    has 3 sigfigs
    .00     has 1 sigfig
    .01     has 1 sigfig
    '''
    def round(value):
        '''code snipped from roundin decimals:
        calculated_value.quantize(Decimal(str(pow(10,-num_digits_to_keep))),
        rounding=ROUND_HALF_EVEN)'''

    def num_all_significant_digits_to_keep(calculated_value, operand_1, operand_2):
        "TODO complete this after add() and mul() work how I want"
        return(None)

    def num_decimal_digits_to_keep(calculated_value, operand_1, operand_2):
        return(min(operand_1.num_significant_decimal_digits,
            operand_2.num_significant_decimal_digits))

    def num_all_significant_digits(value):
        '''Counts number of significant figures in a numeric string.'''
        parsed_value = Rounding_handler_keep_integral_zeroes.get_all_significant_digits(value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_decimal_point(parsed_value) # remove decimal point
        return( len( parsed_value ) )

    def num_significant_decimal_digits(value):
        '''Counts number of significant digits to right of decimal point'''
        return( len(Rounding_handler_keep_integral_zeroes.get_significant_decimal_digits(value)) )

    def get_all_significant_digits(value):
        '''
        Helper function for num_all_significant_digits()
        Remove non digits, undesired zeroes, scientific notation characters,
        but leave the decimal point.
            e.g. -034.5E+3 -> 34.5    or   0.004 -> .4
        '''
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_non_digits(value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_leading_zeroes(parsed_value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_decimal_placeholding_zeroes(parsed_value)
        return( parsed_value )

    def get_significant_decimal_digits(value):
        '''
        Helper function for num_significant_decimal_digits()
        '''
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_non_digits(value)
        parsed_value = Rounding_handler_keep_integral_zeroes.remove_decimal_placeholding_zeroes(parsed_value)
        return( parsed_value.split('.')[1] )



class Rounding_handler_proper(Rounding_handler_keep_integral_zeroes):
    '''
    100     has 1 sigfig
    10.0    has 3 sigfigs
    .00     has 1 sigfig
    .01     has 1 sigfig
    '''
    def get_all_significant_digits(value):
        parsed_value = super().get_all_significant_digits(value)
        parsed_value = Rounding_handler_proper.remove_integral_placeholding_zeroes(parsed_value)
        return( parsed_value )
