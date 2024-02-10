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
    return polynomial.polynomial.polyfromroots(-data)[-2::-1] # The -1 in [-2::-1] reverses the order of the list so that the terms linear in the roots come first. The -2 at the front forced the list to start from the coeffient for x^(n-1). (The coefficient of x^n is always 1 and we dont need it!)
