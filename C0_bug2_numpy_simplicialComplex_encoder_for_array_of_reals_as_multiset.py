#!/usr/bin/env python3

# DO NOT USE! Currently assumed to be invalid.
# This is a re-implementation of C0_bug1_numpy_simplicialComplex_encoder_for_array_of_reals_as_multiset.py using a single list comprehension

# Patrick Kennedy-Hunt
# Christopher Lester

from itertools import pairwise

def encode(data):

    n,m = data.shape
    #print(f"Size (m,n)=({m},{n})")
    _, ans = map_Delta_k_to_the_n_to_c_l_dc_triples(n=n, k=m, delta=vectors_to_delta(data) )

    return ans

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
  

    INPUT REQUIREMENTS:
    * The input k is a non-negative integer
    * The input c is a (possibly empty) list (or set) of (j,i) pairs, with j in [0,n-1] and i in [0,k-1].
    * In the input c there shall be no two pairs (j1,i1) and (j2,i2) such that j1==j2. [Aside: this restricts the length of c to be at most n.]


    What properties should ell satisfy? 
   
    * Even if c is a python list (and so is ordered) it should be considered to represent an unordered mathematical object (set).
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
    
    assert isinstance(k,int), "k should be an integer."
    assert k>=0, "k should be a non-negative integer"
    assert len([j for j,_ in c]) == len({j for j,_ in c}), "no two distinct elements (j1,i1) and (j2,i2) in c should share the same value of j"

    k_vals = [vertex[1] for vertex in c]
    k_vals.sort()  # This divides out S(n)
    return tuple_rank.tuple_rank(k_vals, k)

class Test_Ell(unittest.TestCase):
    def test_sn_perm_collision(self):

        #with lists as inputs:
        self.assertEqual(ell( [(1,5),(2,42),(3,100)], 101),
                         ell( [(7,5),(1,42),(3,100)], 101))  # ( (172) maps 1->7 and 2->1 in S(8) )

        #with sets as inputs:
        self.assertEqual(ell( {(1,5),(2,42),(3,100)}, 101),
                         ell( {(7,5),(1,42),(3,100)}, 101))  # ( (172) maps 1->7 and 2->1 in S(8) )

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

    # REMOVING NEXT TEST AS ell INPUT SPEC PRECULDES ACCEPTING ARGS WITH A REPEATED j AMONG THE (j,i)
    # def test_miss_non_perm(self):
    #     self.assertNotEqual(ell( [(1,5),(2,42),(3,100)], 101),
    #                         ell( [(1,5),(1,42),(3,100)], 101))      # ((1,2,3) cannot map to (1,1,3) under S(8))
    def test_miss_not_same(self):
        self.assertNotEqual(ell( [(1,5),(2,42),(3,100)], 101),
                            ell( [(1,5),(2,42),(3, 90)], 101))      # (90 != 100)
    def test_miss_different_length(self):
        self.assertNotEqual(ell( [(1,5),(2,42),(3,100)], 101),
                            ell( [(3,5),(1,42)        ], 101))      # (different lengths)

def make_flat_sums(n,k,delta, sort=False, prepend_zero=False):
    """
    Conceptually, the dict flat_sums (for k=3) should "represent" the following map
    
    flat_sums = {
      {(0,0)+(0,1)+(0,2)} : delta[(0,0)]+delta[(0,1)]+delta[(0,2)],
      {      (0,1)+(0,2)} :              delta[(0,1)]+delta[(0,2)],
      {            (0,2)} :                           delta[(0,2)],
      {(1,0)+(1,1)+(1,2)} : delta[(1,0)]+delta[(1,1)]+delta[(1,2)],
      {      (1,1)+(1,2)} :              delta[(1,1)]+delta[(1,2)],
      {            (1,2)} :                           delta[(1,2)],
      ...
      ...
      ...
      {(n-1,0)+(n-1,1)+(n-1,2)} : delta[(n-1,0)]+delta[(n-1,1)]+delta[(n-1,2)],
      {        (n-1,1)+(n-1,2)} :                delta[(n-1,1)]+delta[(n-1,2)],
      {                (n-1,2)} :                               delta[(n-1,2)],
    }.

    However, for practial implementation purposes we "represent" the above by the following more abbreviated structure
    (a list of tuples)
    in which for each key the first index is j in [0,n-1], the second index is a tuple containing the i values in the basis sum, 
    I.e. key (j,r) below encodes key sum([ (j,i) for i in r]) above. The example below uses k=3 again
    
    flat_sums = [
      (0, (0,1,2,), delta[(0,0)]+delta[(0,1)]+delta[(0,2)]),
      (0,   (1,2,),              delta[(0,1)]+delta[(0,2)]),
      (0,     (2,),                           delta[(0,2)]),
      (1, (0,1,2,), delta[(1,0)]+delta[(1,1)]+delta[(1,2)]),
      (1,   (1,2,),              delta[(1,1)]+delta[(1,2)]),
      (1,     (2,),                           delta[(1,2)]),
      ...
      ...
      ...
      (n-1, (0,1,2,), delta[(n-1,0)]+delta[(n-1,1)]+delta[(n-1,2)]),
      (n-1,   (1,2,),                delta[(n-1,1)]+delta[(n-1,2)]),
      (n-1,     (2,),                               delta[(n-1,2)]),
    ]


    """
    flat_sums=list([ (j, tuple(range(i_min, k)), sum([delta.get((j,i), 0) for i in range(i_min,k) ])) for j in range(n) for i_min in range(k) ])
    #print("flat_sums unsorted",flat_sums)
    if sort:
        flat_sums = sorted(flat_sums, key=lambda x : (x[2], len(x[1])) ) # Sort by delta sum, but break ties in favour of longer sums
        #print("flat_sums sorted",flat_sums)
    if prepend_zero:
        flat_sums = [ ( None, tuple(), 0) ] + flat_sums
    return flat_sums

class Test_flat_sums(unittest.TestCase):
    def test(self):

        n=4
        k=3

        delta=dict()
        delta[(0,0)]=1
        delta[(0,1)]=4
        delta[(0,2)]=2
        delta[(1,0)]=1
        delta[(1,1)]=54
        delta[(1,2)]=6
        delta[(2,0)]=9
        delta[(2,1)]=10
        delta[(2,2)]=22
        delta[(3,0)]=-2
        delta[(3,1)]=3
        delta[(3,2)]=6

        flat_sums_expected = [
          (0, (0,1,2,), delta[(0,0)]+delta[(0,1)]+delta[(0,2)]),
          (0,   (1,2,),              delta[(0,1)]+delta[(0,2)]),
          (0,     (2,),                           delta[(0,2)]),
          (1, (0,1,2,), delta[(1,0)]+delta[(1,1)]+delta[(1,2)]),
          (1,   (1,2,),              delta[(1,1)]+delta[(1,2)]),
          (1,     (2,),                           delta[(1,2)]),
          (2, (0,1,2,), delta[(2,0)]+delta[(2,1)]+delta[(2,2)]),
          (2,   (1,2,),              delta[(2,1)]+delta[(2,2)]),
          (2,     (2,),                           delta[(2,2)]),
          (3, (0,1,2,), delta[(3,0)]+delta[(3,1)]+delta[(3,2)]),
          (3,   (1,2,),              delta[(3,1)]+delta[(3,2)]),
          (3,     (2,),                           delta[(3,2)]),
        ]
        flat_sums_calculated = make_flat_sums(n,k,delta)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

        flat_sums_expected = [ (None, tuple(), 0), ] + flat_sums_expected

        flat_sums_calculated = make_flat_sums(n,k,delta, prepend_zero = True)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

    def test_with_omitted_zeros(self):

        n=4
        k=3

        delta=dict()
        delta[(0,0)]=1
        # Omit! delta[(0,1)]=4
        delta[(0,2)]=2
        delta[(1,0)]=1
        delta[(1,1)]=54
        delta[(1,2)]=6
        delta[(2,0)]=9
        delta[(2,1)]=10
        delta[(2,2)]=22
        delta[(3,0)]=-2
        delta[(3,1)]=3
        # Omit! delta[(3,2)]=6

        flat_sums_expected = [
          (0, (0,1,2,), delta[(0,0)]+             delta[(0,2)]),
          (0,   (1,2,),                           delta[(0,2)]),
          (0,     (2,),                           delta[(0,2)]),
          (1, (0,1,2,), delta[(1,0)]+delta[(1,1)]+delta[(1,2)]),
          (1,   (1,2,),              delta[(1,1)]+delta[(1,2)]),
          (1,     (2,),                           delta[(1,2)]),
          (2, (0,1,2,), delta[(2,0)]+delta[(2,1)]+delta[(2,2)]),
          (2,   (1,2,),              delta[(2,1)]+delta[(2,2)]),
          (2,     (2,),                           delta[(2,2)]),
          (3, (0,1,2,), delta[(3,0)]+delta[(3,1)]             ),
          (3,   (1,2,),              delta[(3,1)]             ),
          (3,     (2,),                                      0),
        ]
        flat_sums_calculated = make_flat_sums(n,k,delta)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

    def test_one_note_sorted_example(self):

        n=4
        k=3

        delta=dict()
        delta[(0,0)]=0+ 0 # am sneakily writing 0+ 0 for 0.00 to turn decimals into integers, just for testing. This is naughty as delta coords should be in [0,1] but it is OK for this test
        delta[(0,1)]=0+ 3
        delta[(0,2)]=0+22
        delta[(1,0)]=0+00
        delta[(1,1)]=0+11
        delta[(1,2)]=0+10
        delta[(2,0)]=0+10
        delta[(2,1)]=0+00
        delta[(2,2)]=0+50
        delta[(3,0)]=0+ 1
        delta[(3,1)]=0+ 3
        delta[(3,2)]=0+20

        flat_sums_expected = [
          (1,     (2,), 0+10), #                           delta[(1,2)]),
          (3,     (2,), 0+20), #                           delta[(3,2)]),
          (1,   (1,2,), 0+21), #              delta[(1,1)]+delta[(1,2)]),
          (1, (0,1,2,), 0+21), # delta[(1,0)]+delta[(1,1)]+delta[(1,2)]),
          (0,     (2,), 0+22), #                           delta[(0,2)]),
          (3,   (1,2,), 0+23), #              delta[(3,1)]+delta[(3,2)]),
          (3, (0,1,2,), 0+24), # delta[(3,0)]+delta[(3,1)]+delta[(3,2)]),
          (0,   (1,2,), 0+25), #              delta[(0,1)]+delta[(0,2)]),
          (0, (0,1,2,), 0+25), # delta[(0,0)]+delta[(0,1)]+delta[(0,2)]),
          (2,     (2,), 0+50), #                           delta[(2,2)]),
          (2,   (1,2,), 0+50), #              delta[(2,1)]+delta[(2,2)]),
          (2, (0,1,2,), 0+60), # delta[(2,0)]+delta[(2,1)]+delta[(2,2)]),
        ]
        flat_sums_calculated = make_flat_sums(n,k,delta, sort=True)
        self.assertEqual(flat_sums_expected, flat_sums_calculated)

class Test_c_dc_pair_generation(unittest.TestCase):
    def test(self):

        n=4
        k=3
        delta=dict()
        delta[(0,0)]= 0 #0.00
        delta[(0,1)]= 3 #0.03
        delta[(0,2)]=22 #0.22
        delta[(1,0)]= 0 #0.00
        delta[(1,1)]=11 #0.11
        delta[(1,2)]=10 #0.10
        delta[(2,0)]=10 #0.10
        delta[(2,1)]= 0 #0.00
        delta[(2,2)]=50 #0.50
        delta[(3,0)]= 1 #0.01
        delta[(3,1)]= 3 #0.03
        delta[(3,2)]=20 #0.20

        c_dc_pairs_expected = [
                                 ([(0, 2), (1, 2), (2, 2), (3, 2)], 10),
                                 ([(0, 2), (1, 1), (2, 2), (3, 2)], 10),
                                 ([(0, 2), (1, 1), (2, 2), (3, 1)], 1),
                                 ([(0, 2), (1, 0), (2, 2), (3, 1)], 0),
                                 ([(0, 2), (2, 2), (3, 1)], 1),
                                 ([(0, 1), (2, 2), (3, 1)], 1),
                                 ([(0, 1), (2, 2), (3, 0)], 1),
                                 ([(0, 1), (2, 2)], 1),
                                 ([(0, 0), (2, 2)], 0),
                                 ([(2, 2)], 25),
                                 ([(2, 1)], 0),
                                 ([(2, 0)], 10),
                              ]

        c_dc_pairs_calculated = map_Delta_k_to_the_n_to_c_dc_pairs(n,k,delta)
        self.assertEqual(c_dc_pairs_expected, c_dc_pairs_calculated)

        c_dc_pairs_expected = [
                                 ([(0, 2), (1, 2), (2, 2), (3, 2)], 10),
                                 ([(0, 2), (1, 1), (2, 2), (3, 2)], 10),
                                 ([(0, 2), (1, 1), (2, 2), (3, 1)], 1),
                                 ([(0, 2), (2, 2), (3, 1)], 1),
                                 ([(0, 1), (2, 2), (3, 1)], 1),
                                 ([(0, 1), (2, 2), (3, 0)], 1),
                                 ([(0, 1), (2, 2)], 1),
                                 ([(2, 2)], 25),
                                 ([(2, 0)], 10),
                              ]

        c_dc_pairs_calculated = map_Delta_k_to_the_n_to_c_dc_pairs(n,k,delta, prune_zeros=True)
        self.assertEqual(c_dc_pairs_expected, c_dc_pairs_calculated)

def map_Delta_k_to_the_n_to_c_dc_pairs(n , k,  # Only need n and/or k if doing "original initialisation" of x_with_coeffs 
         delta, # Each key in the dict is an (j,i) tuple representing Patrick's e^j_i with j in [0,n-1] and i in [0,k-1].  The associated value is the coefficient of that e^j_i basis vector in the associated element of (\Delta_k)^n.
        # e.g delta = {  
        #     (0,0) : 0.5, (0,1) : 0.2, (0,2) : 0.1,    #a point in the 1st simplex (simplex 0)
        #     (1,2) : 0.25,                             #a point in the 2nd simplex (simplex 1)
        #     (2,0) : 0.1,                              #a point in the 3rd simplex (simplex 2)
        #   }, 
        prune_zeros = False,  # False is recommended default! See comments below.
        ):

    # Pruning zeros is optional as they are technically unnecessasry. However, removing them may also destroy regularity/predictability
    # e.g. people might prefer to see c_dc_pairs always have the same length as the number of non-origin simplex points. 
    # It is also a test on a floating point number, which is a bit silly.  Default should therefore be NOT pruning zeros.

    flat_sums = make_flat_sums(n,k,delta, sort=True)
    print("flat_sums sorted with zero start =",flat_sums)

    dc_vals = [ sum2-sum1 for (j1,i1_vals, sum1),(j2,i2_vals, sum2) in pairwise([(None, tuple(), 0), ]+flat_sums) ]
    print("dc_vals from flat_sums = ")
    [print(_) for _ in dc_vals]

    c_dc_pairs = [ ([ (j,max(moo)) for j in range(n) if (moo:=[ min(iis) for (jj,iis,_) in flat_sums[index:] if jj == j ]) ], dc_vals[index]) for index in range(len(flat_sums)) if not prune_zeros or dc_vals[index] != 0 ]

    print("c_dc_pairs from flat_sums = ")
    [print(_) for _ in c_dc_pairs]

    return c_dc_pairs

def pr(r, big_n):
    return np.power(r, np.arange(1, big_n+1)) # TODO: Ask PK-H whether there is a better final step than pr

def map_Delta_k_to_the_n_to_c_l_dc_triples(n, k, delta):
    c_dc_pairs = map_Delta_k_to_the_n_to_c_dc_pairs(n,k,delta)
    c_l_dc_triples = [ (c, ell(c,k), dc) for (c,dc) in c_dc_pairs ]
    big_n = 2*n*k + 1
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
    if len(vecs)==0:
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


def test_simplex_embedding():
    short = map_Delta_k_to_the_n_to_c_l_dc_triples

    """
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

    enc1 = encode(np.array([[1,2],[1,0],[5,2]]))
    """

    n=4
    k=3
    delta=dict()
    delta[(0,0)]=0.00
    delta[(0,1)]=0.03
    delta[(0,2)]=0.22
    delta[(1,0)]=0.00
    delta[(1,1)]=0.11
    delta[(1,2)]=0.10
    delta[(2,0)]=0.10
    delta[(2,1)]=0.00
    delta[(2,2)]=0.50
    delta[(3,0)]=0.01
    delta[(3,1)]=0.03
    delta[(3,2)]=0.20

    ans8 = short(n=n, k=k, delta=delta)

    """
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
    print("Ans8 was ",ans8)

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

    print("enc1 was ",enc1)
    """

    print()
    print()
    print("Ans8 was ",ans8)
    print("Ans8 was ",ans8[1])


if __name__ == "__main__":
    unittest.main(exit=False)
    test_simplex_embedding()

