
# Encode multiset of reals

def can_encode(m=0, n=0):
    return m==1


def encode(data):
    n=len(data)
    if n==0:
        return []

    m=len(data[0])

    if m!=1:
        throw("Supplied data is not encodable by this encoder.")

    from itertools import combinations
    import numpy as np

    return [ sum( ( np.prod(c)  for c in combinations(data, r+1) )     ) for r in range(n)] 
