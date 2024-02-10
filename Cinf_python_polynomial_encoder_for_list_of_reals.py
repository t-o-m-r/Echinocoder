# Encode list of real numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# Although this implementation claims to only do reals, it does in fact (privately) encode complex lists, albeit to complex outputs.
#
# This implementation as it has TERRIBLE run-time scaling with the length of the imput list, so don't 
# use it unless your your input list has at most ~15 elements.  Use the Cinf_numpy_... version for long lists.
# This implementation can work with arbitrary precision integers, however, which the Cinf_numpy_.... implementation cannot.

name="Cinf_python_polynomial_encoder_for_list_of_reals"

from math import prod
from itertools import combinations
import numpy as np
#import tools


def encode(data):
    return [ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ]
    
    # Alternative
    # 
    # ans = np.array([ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ])
    #
    # All encoders have to output lists of real numbers (at least for now) so:
    #if np.iscomplexobj(ans):
    #  ans=tools.expand_complex_to_real_pairs(ans)
    #
    # return ans



