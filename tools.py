"""
This expands numpy arrays of complex numbers into arrays which are twice as long but which have real parts separated from complex parts.

E.g.:

    [3+4i, 4+2i] -> [3, 4, 4, 2]
"""

import numpy as np

def expand_complex_to_real_pairs(np_array):
    a = np_array.real
    b = np_array.imag
    c = np.empty((a.size+b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c

