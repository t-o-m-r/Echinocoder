# Encode list of real or comlpex numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# or
#
#        [complex(3,4), complex(1,-2), complex(-5,8), ]
#

# Don't use this implementation as it has TERRIBLE run-time scaling with n.  Use the Cinf_np_... version instead. Unless, that is, you want infinite precision integer arithmetic, perhaps.

name="Cinf_py_polynomial_encoder_for_list_of_real_or_complex_numbers"

from math import prod
from itertools import combinations
import numpy as np

def encode(data):
    return np.array([ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ])

