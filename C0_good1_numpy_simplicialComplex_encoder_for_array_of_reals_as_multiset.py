#!/usr/bin/env python3

# USE WITH CAUTION!  No known bugs, but not tested to destruction.
# This is a re-implementation of C0_bug2_numpy_simplicialComplex_encoder_for_array_of_reals_as_multiset.py but aiming to fix the bug in the part of the code which mods out S(n).

# Patrick Kennedy-Hunt
# Christopher Lester

from itertools import pairwise
from tools import invert_perm
import numpy as np
#import tuple_rank
import unittest


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

def ell(c, k, shrink=False):
    """
    The function ell(c, k) can (in principle) be anything that satisfies the properties listed below.
    In practice, presumably some choices are better than others for efficiency reasons or reasons of practicality.
    TODO: Therefore one should experiment with alternatives that go beyond the choices made here!
  

    INPUT REQUIREMENTS:
    * The input k shall be a non-negative integer
    * The input c shall be a (possibly empty) set of (j,i) pairs, with j in [0,n-1] and i in [0,k-1].
    * The set of j values in c shall be identical to set(range(len(c))).  I.e. if there are three pairs in c then one pair will have j=0, one pair will have j=1 and one pair will have j=2.  [Aside: this restricts the length of c to be at most n.]


    What properties should ell satisfy? 
   
    * The input c={(0,4),(2,1)} "represents" the sum of basis vectors e^0_4 + e^2_1 which is clearly the same as e^2_1 + e^0_4 as addition is commutative. This is why c is stored as a set.
    * ell should map every possible c to a natural number.
    * at fixed k, it must be the case that ell(c1,k)==ell(c2,k) <==> c1==c2
    
    E.g. we must have all these equal:
    
        ell( {(1,5),(2,42),(0,100)}, 101)
        ell( {(2,42),(1,5),(0,100)}, 101)

    yet these must all differ:

        ell( {(1,5),(2,42),(0,100)}, 101)     (start)
        ell( {(2,5),(1,42),(0,100)}, 101)     (sets differ in content)
        ell( {(1,5),(2,43),(0,100)}, 101)     (43!=42)
        ell( {(1,5),       (0,100)}, 101)     (sets differ in length)
    
    """
    
    assert isinstance(k,int), "k should be an integer."
    assert k>=0, "k should be a non-negative integer"
    len_c = len(c)
    assert set(range(len_c)) == { j for j,_ in c } # Every j in range(len(c)) should appear once! 
    #print("c was = ",c)

    i_vals_sorted_by_j_vals = [i for _,i in sorted(list(c)) ] # Fortunaltey j comes first in (j,i) so this will work.
    # Note that above we do not bother storing the j values as we know they will be 0,1,..,len(c)-1 given the input preconditions.
    # Thus we will be done if we can hash i_vals_sorted_by_j_vals to a non-colliding value.
    #print("i_vals_sorted_by_j_vals = ",i_vals_sorted_by_j_vals)

    # Either of the two lines below should work identically. Just use one!
    #ell_value = sum(( i*(k**(len_c-1-pos))          for pos,i in enumerate(i_vals_sorted_by_j_vals) ))  +  sum((k**i for i in range(len_c)))
    ell_value_integer = sum(( i*(k**(len_c-1-pos)) + k**pos for pos,i in enumerate(i_vals_sorted_by_j_vals) ))

    #print("ell_value before nonlinear tfm= ",ell_value_integer)
    
    #At this point ell is an integer in 0,1,2,3,4,5, ...
    # We may wish to non-linearly transform it into (-pi/2,pi/2)
   
    if shrink:
        alternate_sign = 2*(ell_value_integer % 2)-1 # Will be +1 or -1 depending on even/oddness of ell_value_ingeger
        ell_value = ell_value_integer * alternate_sign
        ell_value = np.arctan(np.float64(ell_value)/50) # puts ell in (-pi/2,pi/2)
    else:
        ell_value = ell_value_integer

    return ell_value

class Test_Ell(unittest.TestCase):
    def test_sn_perm_collision(self):

        #with lists as inputs:
        self.assertEqual(ell( {(1,5),(2,4),(0,10)}, 11),
                         ell( {(2,4),(1,5),(0,10)}, 11))

    def test_set_function_collision(self):
        self.assertNotEqual(ell( {(1,5),(2,4),(0,10)}, 11), #     (start)
                            ell( {(2,5),(1,4),(0,10)}, 11)) #     (sets differ in content)

        self.assertNotEqual(ell( {(1,5),(2,4),(0,10)}, 11), #     (start)
                            ell( {(1,5),(2,7),(0,10)}, 11)) #     (4!=7)

        self.assertNotEqual(ell( {(1,5),(2,4),(0,10)}, 11), #     (start)
                            ell( {(1,5),      (0,10)}, 11)) #     (sets differ in length)

    def test_intention(self):
        k = 3 

        self.assertEqual(ell(set(), k), 0)                   #   0

        self.assertEqual(ell({(0,0)}, k), 1)                 #   0 + 1
        self.assertEqual(ell({(0,1)}, k), 2)                 #   1 + 1
        self.assertEqual(ell({(0,2)}, k), 3)                 #   2 + 1

        self.assertEqual(ell({(0,0), (1,0)}, k), 4)          #   0 + k**0 + k**1
        self.assertEqual(ell({(0,0), (1,1)}, k), 5)          #   1 + k**0 + k**1
        self.assertEqual(ell({(0,0), (1,2)}, k), 6)          #   2 + k**0 + k**1
        self.assertEqual(ell({(0,1), (1,0)}, k), 7)          #  10 + k**0 + k**1
        self.assertEqual(ell({(0,1), (1,1)}, k), 8)          #  11 + k**0 + k**1
        self.assertEqual(ell({(0,1), (1,2)}, k), 9)          #  12 + k**0 + k**1
        self.assertEqual(ell({(0,2), (1,0)}, k), 10)         #  20 + k**0 + k**1
        self.assertEqual(ell({(0,2), (1,1)}, k), 11)         #  21 + k**0 + k**1
        self.assertEqual(ell({(0,2), (1,2)}, k), 12)         #  22  + k**0 + k**1

        self.assertEqual(ell({(0,0), (1,0), (2,0)}, k), 13)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,0), (2,1)}, k), 14)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,0), (2,2)}, k), 15)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,1), (2,0)}, k), 16)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,1), (2,1)}, k), 17)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,1), (2,2)}, k), 18)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,2), (2,0)}, k), 19)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,2), (2,1)}, k), 20)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,0), (1,2), (2,2)}, k), 21)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,0), (2,0)}, k), 22)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,0), (2,1)}, k), 23)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,0), (2,2)}, k), 24)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,1), (2,0)}, k), 25)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,1), (2,1)}, k), 26)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,1), (2,2)}, k), 27)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,2), (2,0)}, k), 28)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,2), (2,1)}, k), 29)  #   0  + k**0 + k**1 + k**2
        self.assertEqual(ell({(0,1), (1,2), (2,2)}, k), 30)  #   0  + k**0 + k**1 + k**2


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
    flat_sums=[ (j, tuple(range(i_min, k)), sum([delta.get((j,i), 0) for i in range(i_min,k) ])) for j in range(n) for i_min in range(k) ]
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
                                 ({(0, 2), (1, 2), (2, 2), (3, 2)}, 10),
                                 ({(0, 2), (1, 1), (2, 2), (3, 2)}, 10),
                                 ({(0, 2), (1, 1), (2, 2), (3, 1)}, 1),
                                 ({(0, 2), (1, 0), (2, 2), (3, 1)}, 0),
                                 ({(0, 2), (2, 2), (3, 1)}, 1),
                                 ({(0, 1), (2, 2), (3, 1)}, 1),
                                 ({(0, 1), (2, 2), (3, 0)}, 1),
                                 ({(0, 1), (2, 2)}, 1),
                                 ({(0, 0), (2, 2)}, 0),
                                 ({(2, 2)}, 25),
                                 ({(2, 1)}, 0),
                                 ({(2, 0)}, 10),
                              ]

        c_dc_pairs_calculated = make_c_dc_pairs(n,k,delta)
        self.assertEqual(c_dc_pairs_expected, c_dc_pairs_calculated)

        c_dc_pairs_expected = [
                                 ({(0, 2), (1, 2), (2, 2), (3, 2)}, 10),
                                 ({(0, 2), (1, 1), (2, 2), (3, 2)}, 10),
                                 ({(0, 2), (1, 1), (2, 2), (3, 1)}, 1),
                                 ({(0, 2), (2, 2), (3, 1)}, 1),
                                 ({(0, 1), (2, 2), (3, 1)}, 1),
                                 ({(0, 1), (2, 2), (3, 0)}, 1),
                                 ({(0, 1), (2, 2)}, 1),
                                 ({(2, 2)}, 25),
                                 ({(2, 0)}, 10),
                              ]

        c_dc_pairs_calculated = make_c_dc_pairs(n,k,delta, prune_zeros=True)
        self.assertEqual(c_dc_pairs_expected, c_dc_pairs_calculated)

class Test_simplex_eji_ordering_generation(unittest.TestCase):
    def test(self):

        c_bits_and_null = [
                             {(0, 2), (1, 2), (2, 2), (3, 2)},
                             {(0, 2), (1, 1), (2, 2), (3, 2)},
                             {(0, 2), (1, 1), (2, 2), (3, 1)},
                             {(0, 2), (1, 0), (2, 2), (3, 1)},
                             {(0, 2), (2, 2), (3, 1)},
                             {(0, 1), (2, 2), (3, 1)},
                             {(0, 1), (2, 2), (3, 0)},
                             {(0, 1), (2, 2)},
                             {(0, 0), (2, 2)},
                             {(2, 2)},
                             {(2, 1)},
                             {(2, 0)},
                             set(),
                          ]
        ordering_calculated = make_simplex_eji_ordering(c_bits_and_null)

        ordering_expected = [
                             (1, 2),
                             (3, 2),
                             (1, 1),
                             (1, 0),
                             (0, 2),
                             (3, 1),
                             (3, 0),
                             (0, 1),
                             (0, 0),
                             (2, 2),
                             (2, 1),
                             (2, 0),
                          ]
        self.assertEqual(ordering_calculated, ordering_expected)


class Test_perm_detection(unittest.TestCase):
    def test(self):

        simplex_eji_ordering = [ (1, 2), (3, 2), (1, 1), (0, 2), (3, 1), (3, 0), (0, 1), (1, 0), (0, 0), (2, 2), (2, 1), (2, 0), ]

        simple_ordering_on_j_vals_from_left_expected = [ 1, 3, 0, 2 ] # j vals read from left, ignoring repeats
        simple_ordering_on_j_vals_from_right_expected = [ 2, 0, 1, 3 ] # j vals read from right, ignoring repeats

        ordering_from_left_calculated = make_perm_from_simplex(simplex_eji_ordering)
        ordering_from_right_calculated = make_perm_from_simplex(simplex_eji_ordering, from_right=True)

        self.assertEqual(simple_ordering_on_j_vals_from_left_expected, ordering_from_left_calculated)
        self.assertEqual(simple_ordering_on_j_vals_from_right_expected, ordering_from_right_calculated)

def make_perm_from_simplex(simplex_eji_ordering, from_right=False):
    # Note that setting from_right does not (in general) reverse the answer even though it reverses the input.
    # I.e. perm_from_right(ordering)[::-1] is not in general the same as perm_from_left(ordering[::-1]).
    if from_right:
      simplex_eji_ordering=simplex_eji_ordering[::-1]
    return list({ j[0] : None for j in simplex_eji_ordering  }) # Uses insertion order preservation


def make_c_dc_pairs(n , k,  # Only need n and/or k if doing "original initialisation" of x_with_coeffs 
         delta, # Each key in the dict is an (j,i) tuple representing Patrick's e^j_i with j in [0,n-1] and i in [0,k-1].  The associated value is the coefficient of that e^j_i basis vector in the associated element of (\Delta_k)^n.
        # e.g delta = {  
        #     (0,0) : 0.5, (0,1) : 0.2, (0,2) : 0.1,    #a point in the 1st simplex (simplex 0)
        #     (1,2) : 0.25,                             #a point in the 2nd simplex (simplex 1)
        #     (2,0) : 0.1,                              #a point in the 3rd simplex (simplex 2)
        #   }, 
        prune_zeros = False,  # False is recommended default! See comments below.
        ):
    """
    We output a list of c_dc_pairs.  Each pair (c,dc) contains a simplex vertex, c, together with a coefficient, dc.
    The simplex vertex, c, is coded as a list of (j,i) values representing e^j_i, i.e. the ith basis vector of the j-th simplex.
    E.g. if the simplex vertex is c=[(0,1),(2,2)] then c represents e^0_1+e^2_2. 
    The coefficient dc,  attached to c, says how much of c is needed to represent the component of delta in that direction.
    """

    """
    Pruning entries with dc=0 might seem like a good idea.  However:

       (1) pruning zeros may also destroy regularity/predictability;  e.g. people might prefer to see c_dc_pairs always have the same length as the number of non-origin simplex points.
       (2) pruning zeros requires  a test for equality on a floating point number, which is a bit silly.  Default should therefore be NOT pruning zeros,
       (3) worst of all, pruning zeors makes it impossible to identify and canonicalise the simplex vertices.

       Hence, do not prune zeros unless you have a good reason!
    """

    flat_sums = make_flat_sums(n,k,delta, sort=True)
    #print("flat_sums sorted with zero start =",flat_sums)

    dc_vals = [ sum2-sum1 for (j1,i1_vals, sum1),(j2,i2_vals, sum2) in pairwise([(None, tuple(), 0), ]+flat_sums) ]
    #print("dc_vals from flat_sums = ")
    #[print(_) for _ in dc_vals]

    c_dc_pairs = [ ({ (j,max(moo)) for j in range(n) if (moo:=[ min(iis) for (jj,iis,_) in flat_sums[index:] if jj == j ]) }, dc_vals[index]) for index in range(len(flat_sums)) if not prune_zeros or dc_vals[index] != 0 ] # See set note below
    """A set rather than a list is used to hold the coordinate vectors because later we want to find out "elements in one set not in another" ... and so if we had used lists we would have to construct a set from a list later anyway.  Fortunately the objects represented are sets anyway (they represent sums of dissimilar basis elements which are vertices, and sums are order independent).  The set creation comprehension does not produce duplicate elements squashed by the set, though, so if it's later needed they could be changed back to a list here (instead of set) so long as the later set-difference calculation is done some other way."""

    #print("c_dc_pairs from flat_sums = ")
    #[print(_) for _ in c_dc_pairs]

    return c_dc_pairs

def pr(r, big_n):
    # Method below makes negative numbers from positive integer r if r is big enough!  Floating point wrap around! Must make r real
    return np.power(np.float64(r), np.arange(big_n)) # Starting at zeroeth power so that r can be both zero and non-zero without constraint.

def make_simplex_eji_ordering(c_bits_and_null):
    """
    The following simplex_eji_ordering contains the implied basis element ordering (greatest first)
    which defined the simplex in which we the point delta stands.
    """
    simplex_eji_ordering = [ (c1-c2).pop() for c1,c2 in pairwise(c_bits_and_null) ] # The set c1-c2 shuld contain only one element, so pop() should return it.
    return simplex_eji_ordering

def map_Delta_k_to_the_n_to_c_l_dc_triples(n, k, delta):
    c_dc_pairs = make_c_dc_pairs(n,k,delta)
 
    c_bits_and_null = [ c for c,_ in c_dc_pairs ] + [set()]
    #print("c_bits (before modding by S(n)) =")
    #[ print(c) for c in c_bits_and_null ]

    """
    The following simplex_eji_ordering contains the implied basis element ordering (greatest first)
    which defined the simplex in which we the point delta stands.
    """
    simplex_eji_ordering = make_simplex_eji_ordering(c_bits_and_null)
    #print("simplex_eji_ordering (before mod S(n)) =")
    #[ print(eji) for eji in simplex_eji_ordering ]

    # We must canonicalise the simplex by detecting and modding out the relevant perm of S(n).

    # First detect the perm needed to take our simplex to canonical form:
    perm = make_perm_from_simplex(simplex_eji_ordering, from_right=True) # It is not critical whether we come from right or left, since any canonical form will do. I choose from_right as it matches the conventin I used in some OneNote nootbooks while I was getting to grips with things. from_left would be faster as no need to reverse a list internally.  Consider moving to from_left later.
    #print("perm = ",perm)
    
    # Actually we need the inverse perm!
    inverse_perm = invert_perm(perm)
    #print("inverse perm = ", inverse_perm)

    # Now 'canonicalise' the vertices in c_dc_pairs using that perm:
    c_dc_pairs_after_mod_Sn = [ ({ (inverse_perm[j], i) for (j,i) in c }, dc)  for (c,dc) in c_dc_pairs   ]
    #print("c_dc_pairs (after modding by S(n)) =")
    #[ print(c) for c in c_dc_pairs_after_mod_Sn ]
    
    # Don't actually need the next thing -- but compute it for debug purposes "just in case"
    simplex_eji_ordering_after_mod_Sn = [ (inverse_perm[j], i) for (j,i) in simplex_eji_ordering ] 
    #print("simplex_eji_ordering (after mod S(n)) =")
    #[ print(eji) for eji in simplex_eji_ordering_after_mod_Sn ]

    shrink = True
    c_l_dc_triples = [ (c, ell(c,k,shrink=shrink), dc) for (c,dc) in c_dc_pairs_after_mod_Sn ]
    #print("c_l_dc_triples (after modding by S(n)) =")
    #[ print(c) for c in c_l_dc_triples ]
    big_n = 2*n*k + 1
    # Please someone re-implement this dot product without so many comprehensions ... or at any rate BETTER:
    # Want output here to be sum_i pr(r_i, big_n) x_i)
    # where, in effect, r_i and x_i would be defined by
    # [ blah for _, r_i, x_i in c_l_dc_triples ]

    #print("pr(20)=",pr(20,big_n))
    point_in_R_bigN = sum([d * pr(r, big_n) for _, r, d in c_l_dc_triples]) + np.zeros(big_n)  # Addition of zero term at end ensures that we still get a zero vec (not 0) in the event that c_l_dc_triples is empty!

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
    test_simplex_embedding()
    unittest.main(exit=False)

