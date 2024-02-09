
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

    import math

    from itertools import combinations
    #from math import prod
    def prod(x):
       import math
       print("MOO: ",x)
       print("COW: ",math.prod(x))
       return math.prod(x)

    def flatten(xss):
        return [x for xs in xss for x in xs]

    return [ ( prod(c)  for c in combinations([d[0] for d in data], r+1)      ) for r in range(n) ] 
