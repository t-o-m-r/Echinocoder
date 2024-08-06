# Encode list of n real numbers treated as an element of a realprojectiveplane.
#
# This particular implentation explots a complex trick which (when n is even and greater than 0) allows the encoding save one real number over that required by trhe underlying regular implementation.
#
# I.e. the method encodes to:
#
#       0 reals when n is 0
#       2n-2 reals when n is even and n>0     (A SAVING OF ONE REAL!!)
#       2n-1 reals when n is odd.
#
# E.g. this method can encode an ordered list like this
#
#        x = [3,4,-2,5]
#
# which is deemed to be equivalent to its negation:
#
#        -x = [-3,-4,2,-5].
#
#

import numpy as np
import tools
import Cinf_python_regular_encoder_for_list_of_realsOrComplex_as_realOrComplexprojectiveplane as underlying_encoder

def encode(data):
    # data=np.asarray(data)
    return np.asarray([ np.trace(np.flipud(np.outer(data,data)),diag) for diag in range(1-len(data),len(data)) ])
    
# Just for testing/debug:
if __name__ == "__main__":
  for data in (np.asarray([3,4,-2,5]), np.asarray([3,4,-2])):
    print()
    complex_data = tools.real_pairs_to_complex_zip(data)
    complex_encoding = underlying_encoder.encode(complex_data)
    real_encoding = tools.expand_complex_to_real_pairs(complex_encoding)
    # Now trim off last entry but ONLY IF we know it will be zero by construction -- this is when the data has an odd length
    if len(data)%2 == 1:
        real_encoding = real_encoding[:-1]

    print("data ",data)
    print("complex_data ",complex_data)
    print("complex_encoding",complex_encoding)
    print("real_encoding ",real_encoding)
    # Should print
    """
    input  [ 3  4 -2  5]
    reals  [ 3 -2]
    images  [4 5]
    data  [ 3  4 -2  5]
    complex_data  [ 3.+4.j -2.+5.j]
    complex_encoding [ -7.+24.j -52.+14.j -21.-20.j]
    real_encoding  [ -7.  24. -52.  14. -21. -20.]
    
    input  [ 3  4 -2]
    reals  [ 3 -2]
    images  [4 0]
    data  [ 3  4 -2]
    complex_data  [ 3.+4.j -2.+0.j]
    complex_encoding [ -7.+24.j -12.-16.j   4. +0.j]
    real_encoding  [ -7.  24. -12. -16.   4.]
    """

