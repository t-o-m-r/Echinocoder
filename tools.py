"""
This expands numpy arrays of complex numbers into arrays which are twice as long but which have real parts separated from complex parts.
"""

import numpy as np


def expand_complex_to_real_pairs(array):
    a=array.real
    b=array.imag
    c=np.empty((a.size+b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c
