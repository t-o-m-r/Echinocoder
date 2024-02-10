# Encode list of real or comlpex numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# or
#
#        [complex(3,4), complex(1,-2), complex(-5,8), ]
#

name="Cinf_np_polynomial_encoder_for_list_of_real_or_complex_numbers"

from numpy import polynomial

def encode(data):
    return polynomial.polynomial.polyfromroots(data)
