# Encode list of real or comlpex numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# or
#
#        [complex(3,4), complex(1,-2), complex(-5,8), ]
#

from math import prod
from itertools import combinations, tee

def encode(data):
    data=list(data)
    n=len(data)
    return [ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(n) ] 
