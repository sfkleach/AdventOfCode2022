from operator import mul
from functools import reduce

def product( iterable ):
    """Finds the multiplicative product of a sequence of numbers"""
    return reduce( mul, iterable, 1 )
