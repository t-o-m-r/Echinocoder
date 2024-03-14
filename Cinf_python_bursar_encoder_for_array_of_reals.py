# Encode list of real numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [[3,2],[4,1],[-2,1]]
#
# Although this implementation claims to only operate on arrays of reals, it does in fact (privately) encode complex arrays, albeit to complex outputs.
#
name="Cinf_python_bursar_encoder_for_array_of_reals"

from math import prod
#from itertools import combinations
#import numpy as np
#import tools
from sympy import Poly, abc

def encode(data):
    
    print("Data is")
    print(data)

    n = len(data)
    if n==0:
        return []

    m = len(data[0])
    if m==0:
        return []

    polys = [ Poly(vector, abc.x)+Poly(abc.y) for vector in data ]

    print("polys",polys)

    product = prod(polys)
    print ("Product",product)

    # extract coeffs from product
    for c in range(1,n+1):
         yPower = n-c
         for xPower in range(c*(m-1)+1):
             coeff = product.coeff_monomial((abc.x)**xPower * (abc.y)**yPower)
             print(coeff)

    #xPolys = [ np.polynomial.Polynomial(vector) for vector in data ] 
    #print("x polynomials are: ")
    #for xPoly in xPolys:
    #    print (xPoly)
    # 
    #n=len(data)

    return [1,2,3]
    
    #return [ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ]

    # return [ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ]
    
    # Alternative
    # 
    # ans = np.array([ sum( [ prod(c)  for c in combinations(data, r+1) ] ) for r in range(len(data)) ])
    #
    # All encoders have to output lists of real numbers (at least for now) so:
    #if np.iscomplexobj(ans):
    #  ans=tools.expand_complex_to_real_pairs(ans)
    #
    # return ans



