# Encode list of real  numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#

from math import prod
from itertools import combinations, tee

def encode(data):
    return sorted(data)
