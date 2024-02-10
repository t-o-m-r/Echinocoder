# Encode list of real or comlpex numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# or
#
#        [complex(3,4), complex(1,-2), complex(-5,8), ]
#

name="Cinf_py_polynomial_encoder_for_list_of_real_or_complex_numbers"

from math import prod
from itertools import combinations

def encode(data):
    return [ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ] 

