import numpy as np

def expand_complex_to_real_pairs(np_array):
    """
    This function expands numpy arrays of complex numbers into arrays which are twice as long but which have real parts separated from complex parts.
    E.g.:   [3+4i, 4+2i] -> [3, 4, 4, 2]
    Its inverse is "real_pairs_to_complex_zip".
    """

    a = np_array.real
    b = np_array.imag
    c = np.empty((a.size+b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c

def real_pairs_to_complex_zip(np_array):
    """
    This function zips adjacent reals in an array of length n into complex numbers in an array of length floor(n/2).
    E.g.:  [3, 4, 4, 2] -> [3+4i, 4+2i]
    or:    [3, 4, 4,  ] -> [3+4i, 4   ]
    Its inverse is "expand_complex_to_real_pairs".
    """
   reals = np_array[0::2]
   imags = np_array[1::2]
   if len(imags)<len(reals):
      imags = np.append(imags, [0])
   print("input ",np_array)
   print("reals ",reals)
   print("images ",imags)
   return reals+1j*imags


