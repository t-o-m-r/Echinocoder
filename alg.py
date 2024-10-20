#!/opt/local/bin/python3

# Patrick Kennedy-Hunt
# Christopher Lester

# Where used in this file the expression Deltak (or $\Delta^k$ in TeX) 
# refers to the space inside a unit k-simplex.
# A point in Deltak could be parameterised by  k real numbers: 
#
#      x_0, x_1, ... , x_(k-1)
#
# with the property that:
#
#      0 <= x_i <= 1 for all i
#
# and for which
#
#      sum_i x_i <= 1.
#
# The implementation below  also handles points that live inside spaces which are
# products of n copies of Deltak. These would be in $(\Delta^k)^n$ in TeX, but
# in the sourcecode we term this space Deltakn.  
#
# For practical reasons, the implementation below mostly stores points in Deltak
# or in Deltakn not as lists, i.e. not as
#
#  x = [x_0, x_1, ... , x_(k-1)]
#
# but instead stores them as dictionaries mapping key index pairs (j,i) to the 
# simplex coordinates. In these key index pairs (j,i) the value j in [0,n-1] 
# indexes the copy of Deltak within Dektakn,  and the i value in [0,k-1] 
# indexes the coordinate position within Deltak.
#
# For examplex:, for n=2 and k=2 ...
#
# a point x within the first Deltak within Deltakn might be stored as
#
#          x = { (0,0):0.25,  (0,1):0.50, (0,2):0.10, }
#
# and a point y within the second Deltak within Deltakn might be stored as
#
#          y = { (1,0):0.05, (1,1):0.00,  (1,2):0.90, }
#
# or equivalentlay (since zero coefficients may be omitted) as
#
#          y = { (1,0):0.05,              (1,2):0.90, }
#
# and a point delta = x*y  within Detlakn would be stored as
#
#          delta = { **x, **y }
#                = { 
#                    (0,0):0.25,  (0,1):0.50, (0,2):0.10, 
#                    (1,0):0.05,              (1,2):0.90, 
#                  }.
#

import numpy as np
import tuple_rank
import unittest

def ell(c, k):
    """
    The function ell(c, k) can (in principle) be anything that satisfies the properties listed below.
    In practice, presumably some choices are better than others for efficiency reasons or reasons of practicality.
    TODO: Therefore one should experiment with alternatives that go beyond the choices made here!
    
    What properties should ell satisfy? 
    
    * each c is a (possibly empty) list (or set) of (j,i) pairs, with j in [0,n-1] and i in [0,k-1].
      Even if c is a python list (and so is ordered) it is representing an unordered mathematical object (set).
    
    * ell should map every possible c to a natural number.
    * for same k, inputs c1 and c2 differing only by a permutation of the j's among n elements must map to the same number (i.e. must collide).
    * for same k, all other collisions are forbidden.
    * Thus ell should be a function on C mod S(n).
    
    E.g. we must have all these equal:
    
        ell( [(1,5),(2,42),(3,100)], 101)
        ell( [(7,5),(1,42),(3,100)], 101)
    
    since 1,2,3 can be mapped to 7,1,3 by the S8 perm 
    
            (0,1,2,3,4,5,6,7) -> (0,7,1,3,4,5,6,2)

    which looks like (172) in cycle notation.

    We must also have these equal:

        ell( [(1,5),(2,42),(3,100)], 101)
        ell( [(2,42),(1,5),(3,100)], 101)

    since ell must be a set function.

    In contrast:
    
        ell( [(1,5),(2,42),(3,100)], 101)
    
    should not collide with any of:
    
        ell( [(1,5),(1,42),(3,100)], 101)      ((1,2,3) cannot map to (1,1,3) under S(8))
        ell( [(1,5),(2,42),(3, 90)], 101)      (90 != 100)
        ell( [(3,5),(1,42)],       , 101)      (different lengths)
    
    etc, to name just a few of the infinite number of things which must be avoided.
    """
        
    k_vals = [vertex[1] for vertex in c]
    k_vals.sort()  # This divides out S(n)
    return tuple_rank.tuple_rank(k_vals, k)

class Test_Ell(unittest.TestCase):
    def test_sn_perm_collision(self):
        # since (172) (cycle notation) is a perm in S(8):

        #with lists as inputs:
        self.assertEqual(ell( [(1,5),(2,42),(3,100)], 101),
                         ell( [(7,5),(1,42),(3,100)], 101))

        #with sets as inputs:
        self.assertEqual(ell( {(1,5),(2,42),(3,100)}, 101),
                         ell( {(7,5),(1,42),(3,100)}, 101))

    def test_set_function_collision(self):
        # With lists as inputs:
        self.assertEqual(ell( [(1,5),(2,42),(3,100)], 101),
                         ell( [(2,42),(1,5),(3,100)], 101))
        # With sets as inputs:
        self.assertEqual(ell( {(1,5),(2,42),(3,100)}, 101),
                         ell( {(2,42),(1,5),(3,100)}, 101))
        # With mix of inputs:
        self.assertEqual(ell( [(1,5),(2,42),(3,100)], 101),
                         ell( {(2,42),(1,5),(3,100)}, 101))

    def test_miss_non_perm(self):
        self.assertNotEqual(ell( [(1,5),(2,42),(3,100)], 101),
                            ell( [(1,5),(1,42),(3,100)], 101))      # ((1,2,3) cannot map to (1,1,3) under S(8))
    def test_miss_not_same(self):
        self.assertNotEqual(ell( [(1,5),(2,42),(3,100)], 101),
                            ell( [(1,5),(2,42),(3, 90)], 101))      # (90 != 100)
    def test_miss_different_length(self):
        self.assertNotEqual(ell( [(1,5),(2,42),(3,100)], 101),
                            ell( [(3,5),(1,42)        ], 101))      # (different lengths)

def map_Delta_k_to_the_n_to_c_dc_pairs(#n=3,k=3,  # Only need n and/or k if doing "original initialisation" of x_with_coeffs 
         delta = dict(), # Each key in the dict is an (j,i) tuple representing Patrick's e^j_i with j in [0,n-1] and i in [0,k-1].  The associated value is the coefficient of that e^j_i basis vector in the associated element of (\Delta_k)^n.
        # e.g delta = {  
        #     (0,0) : 0.5, (0,1) : 0.2, (0,2) : 0.1,    #a point in the 1st simplex (simplex 0)
        #     (1,2) : 0.25,                             #a point in the 2nd simplex (simplex 1)
        #     (2,0) : 0.1,                              #a point in the 3rd simplex (simplex 2)
        #   }, 
        ):

    c_dc_pairs = []

    print("delta",delta)


    if False:
        # Original initialisation. If using this pass n and k to the algorithm

        # Set up initial value of x based on n, k and delta.
        # This is the only place where n or k is used.

        x_with_coeffs = {  (j,k-1):delta.get((j,k-1),0)  for j in range(n) } 
    else:


        # n-and-k-independent initialisation
        if delta:
           j_vals = {j for (j,i) in delta.keys() }
           largest_j = max(j_vals)
           largest_i_for_j = {  j:max([ i for (jj,i) in delta.keys() if jj == j ])   for j in j_vals }
           x_with_coeffs = {  (j,largest_i_for_j[j]):delta[(j,largest_i_for_j[j])]  for j in j_vals } 
        else:
           x_with_coeffs = dict()

    while x_with_coeffs:
        print("Iteration! =====")
        print("delta",delta)
        print("x_with_coeffs",x_with_coeffs)

        e = min(x_with_coeffs, key=x_with_coeffs.get)
        dx = x_with_coeffs[e]
        z=e[0] # z is the j-val of the element of x with the smallest coefficient
        print("smallest: e=",e,"coeff=",dx, "z=",z)

        if dx<0:
            # dx should never be negative.
            print("ERROR: or unexpected numerical precision concern since dx=",dx,"<0.")
            raise Exception("IMPLEMENTATION ERROR")

        if dx>0:
            # Grow the c_dc_pairs list
            c = list(x_with_coeffs.keys()) # could use list or set in the implementation ... it doesn't really matter ... but the object represented is a set
            c_dc_pairs.append((c, dx)) 
            print("grew c_dc_pairs")
            print("c_dc_pairs=",c_dc_pairs)

            # trim delta
            for pair,val in list(delta.items()):
                 if pair in c:
                     if val == dx:
                        del delta[pair]
                     elif val>dx:
                        delta[pair] = val-dx
                     else:
                        print("val=",val,"dx=",dx)
                        raise Exception("IMPLEMENTATION ERROR! Should not have val<dx.")

        # trim and update x_with_coeffs:

        del x_with_coeffs[e] # since this part should be gone.  Needed by next line!
        # Set up new keys:
        new_keys = list(x_with_coeffs.keys()) # Will not contain e.
        if e[1]>0:
            new_e = (z, e[1]-1)
            new_keys.append(new_e)

        # refresh x_with_coeffs:
        x_with_coeffs = { new_key:delta.get(new_key,0)  for new_key in new_keys } 
           
    # We are done:        
    return c_dc_pairs

def pr(r, big_n):
    return np.power(r, np.arange(1, big_n+1)) # TODO: Ask PK-H whether there is a better final step than pr

def map_Delta_k_to_the_n_to_c_l_dc_triples(n, k, delta):
    c_dc_pairs = map_Delta_k_to_the_n_to_c_dc_pairs(delta=delta)
    c_l_dc_triples = [ (c, ell(c,k), dc) for (c,dc) in c_dc_pairs ]
    big_n = n*k+1
    # Please someone re-implement this dot product without so many comprehensions ... or at any rate BETTER:
    # Want output here to be sum_i pr(r_i, big_n) x_i)
    # where, in effect, r_i and x_i would be defined by
    # [ blah for _, r_i, x_i in c_l_dc_triples ]
    # Help Jeremy!

    point_in_R_bigN = sum([d * pr(r, big_n) for _, r, d in c_l_dc_triples]) + pr(0, big_n) # Addition of zero term at end ensures that we still get a zero vec (not 0) in the event that c_l_dc_triples is empty!

    return c_l_dc_triples, point_in_R_bigN 

def vector_to_simplex_point(vec):
    k = len(vec)
    vec = np.array(vec)
    return 1.0/(k*(1.0+np.power(2.0,vec))) # TODO: This somewhat crude parametrisation does not use the WHOLE of the simplex -- so it's a bit wasteful. It also has terrible dynamic range problems and even unit issues. Might want to address all of these points with a better mapping.

def vectors_to_delta(vecs):
    n=len(vecs)
    delta = {}
    if not vecs:
        return delta
    # vecs is not empty
    k = len(vecs[0])
    for j in range(n):
        vec = vecs[j]
        simplex_point = vector_to_simplex_point(vec)
        k_this = len(vec)
        if k!=k_this:
            raise Exception("Vectos supplied to vectors_to_delta are not all the same dimension!")
        for i in range(k):
            delta[(j,i)]=simplex_point[i]
    return delta


def unit_test_simplex_embedding():
    short = map_Delta_k_to_the_n_to_c_l_dc_triples

    ans1 = short(n=3, k=3, 
                 delta = {  (0,1) : 0.5, (1,2) : 0.25 }, )

    # Next three all similar to each other.
    ans2a = short(n=3, k=3, 
                  delta = {  (0,2) : 0.5, (1,2) : 0.25, (2,2):0.1 }, )
    ans2b = short(n=3, k=3, 
                  delta = {  (0,2) : 0.5, (1,2) : 0.25, (2,2):0.1,  (1,1):0.0001}, )
    ans2c = short(n=3, k=3, 
                  delta = {  (0,2) : 0.5, (1,2) : 0.25, (2,2):0.1001,  }, )

    # Perm invariance
    ans3c1 = short(n=3, k=3, 
                   delta = {  (0,2) : 0.5, (1,0):0.001, (1,2) : 0.25, (2,2):0.1001,  }, )
    ans3c2 = short(n=3, k=3, 
                   delta = {  (1,2) : 0.5, (0,0):0.001, (0,2) : 0.25, (2,2):0.1001,  }, )

    # Trick case:
    ans4 = short(n=3, k=3, 
             delta = {
             (0,0) : 0.5, (0,1) : 0.2, (0,2) : 0.1,    #a point in the 1st simplex
             (1,2) : 0.25,                             #a point in the 2nd simplex 
             (2,0) : 0.1,                              #a point in the 3rd simplex
             })

    # Trick case:
    ans5 = short(n=7, k=3, 
             delta = {
             (0,0) : 0.5, (0,1) : 0.2, (0,2) : 0.1,    #a point in the 1st simplex
             (1,2) : 0.25,                             #a point in the 2nd simplex 
             (2,0) : 0.1,                              #a point in the 3rd simplex
             })

    # Zero cases:
    ans6a = short(n=7, k=3, 
                  delta = { (0,1) : 0.0, (1,2) : 0.0, })
    ans6b = short(n=7, k=3,
                  delta = dict()                       )
    ans6c = short(n=7, k=3,
                  delta = vectors_to_delta( [] )       )

    ans7 = short(n=3, k=2,
                  delta = vectors_to_delta( [
                     np.array([1,2]), # k-vector 1 of n
                     np.array([1,0]), # k-vector 2 of n
                     np.array([5,2]), # k-vector 3 of n
                  ] )
                )

    print("Ans1 was ",ans1)
    print("Ans2a was ",ans2a)
    print("Ans2b was ",ans2b)
    print("Ans2c was ",ans2c)
    print("Ans3c1 was ",ans3c1)
    print("Ans3c2 was ",ans3c2)
    print("Ans5 was ",ans5)
    print("Ans6a was ",ans6a)
    print("Ans6b was ",ans6b)
    print("Ans6c was ",ans6c)
    print("Ans7 was ",ans7)

    print("Ans1 was ",ans1[1])
    print("Ans2a was ",ans2a[1])
    print("Ans2b was ",ans2b[1])
    print("Ans2c was ",ans2c[1])
    print("Ans3c1 was ",ans3c1[1])
    print("Ans3c2 was ",ans3c2[1])
    print("Ans5 was ",ans5[1])
    print("Ans6a was ",ans6a[1])
    print("Ans6b was ",ans6b[1])
    print("Ans6c was ",ans6c[1])
    print("Ans7 was ",ans7[1])
    
if __name__ == "__main__":
    unittest.main()
    unit_test_simplex_embedding()

