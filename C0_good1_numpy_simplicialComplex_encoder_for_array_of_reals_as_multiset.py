#!/usr/bin/env python3

from sys import version_info

import numpy

if not version_info >= (3, 7):
    assert False, "We need at least python 3.7 as we rely on dictionaries being ordered!"

# USE WITH CAUTION!  No known bugs, but not tested to destruction.
# This is a re-implementation of C0_bug2_numpy_simplicialComplex_encoder_for_array_of_reals_as_multiset.py but aiming to fix the bug in the part of the code which mods out S(n).

# Patrick Kennedy-Hunt
# Christopher Lester

from itertools import pairwise
#from tools import invert_perm
import numpy as np
#import tuple_rank
import unittest
from dataclasses import dataclass, field


def encode(data, use_n2k2_optimisation=False):

    n,m = data.shape
    #print(f"Size (m,n)=({m},{n})")
    _, ans = map_Delta_k_to_the_n_to_c_l_dc_triples(n=n, k=m, delta=vectors_to_delta(data), use_n2k2=use_n2k2_optimisation)

    #Interleave the two outputs in debug mode:
    # _, ans2 = map_Delta_k_to_the_n_to_c_l_dc_triples(n=n, k=m, delta=vectors_to_delta(data), use_n2k2=True)
    #return [ val for pair in zip(ans,ans2) for val in pair ]

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
# For example:, for n=2 and k=2 ...
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

@dataclass
class Position_within_Simplex:
    """
    A point inside a k-simplex is defined by k reals values delta_i with the property that:

    * 0 <= delta_i for all i in 0,1,2,...,k-1, and
    * sum_{i=0}^{k-1} delta_i <= 1.

    The purpose of this class is to hold and manipulate such delta_i, and to manage conversions
    between such things and other coordinate systems.
    """
    _np_ar : numpy.array

    def __getitem__(self, item):
        return self._np_ar[item]

    def __init__(self, x):
        self._np_ar = np.array(x)

    def __eq__(self, other):
        return (self._np_ar == other._np_ar).all()

    def check_valid(self):
        #print("  XOO", self._np_ar)
        assert sum(self._np_ar) <= 1, "Total of simplex coordinates should not exceed 1."
        for coeff in self._np_ar:
            #print("    YOO", coeff)
            assert coeff >= 0, "Every simplex coordinate should be non-negative."

@dataclass
class Position_within_Simplex_Product:
    """
    Conceptually this holds "n" copies of Point_in_simplex.
    However, for performance reasons we hold it as a numpy array, with
    first index j in [0,n-1] identified the product, and
    second index i in [0,k-1] identifies the position within the j-th simplex.
    """
    _np_ar : numpy.array

    def __init__(self, x):
        #print("CONSTRUCTING 1")
        if isinstance(x, np.ndarray):
            #print("CONSTRUCTING 2")
            self._np_ar = x
        elif isinstance(x, list) and x and isinstance(x[0], Position_within_Simplex):
            #print("CONSTRUCTING 3")
            self._np_ar = np.array([pos._np_ar for pos in x])
        else:
            # Hope for best:
            #print("CONSTRUCTING 4")
            self._np_ar = np.array(x)

    def __getitem__(self, item):
        """
        If called with one index, get Position_within_Simplex.
        If called with two indices, get coeff directly from within Position_within_Simplex.
        """
        if isinstance(item, tuple):
            # Get coeff directly from within Position_within_Simplex.
            return self._np_ar[item]

        # Get Position_within_Simplex.
        return Position_within_Simplex(self._np_ar[item])

    def check_valid(self):
        for pos in self._np_ar:
            Position_within_Simplex(pos).check_valid()

from collections import namedtuple
Eji = namedtuple("Eji", ["j", "i"])

@dataclass
class Eji_Ordering:
    """Class to hold eij orderings (biggest first)."""
    _eji_list: list[Eji]
    def check_valid(self):
        j_vals = [e.j for e in self._eji_list]
        i_vals = [e.i for e in self._eji_list]

        presumed_n = max(j_vals, default=-1)+1
        presumed_k = max(i_vals, default=-1)+1
        assert presumed_n*presumed_k == len(self._eji_list), "Expect n*k entries in the ordering!"
        assert set(self._eji_list) == {Eji(j, i)
                                       for j in range(presumed_n)
                                       for i in range(presumed_k)}, "Each Eji value shjould appear once!"

@dataclass
class Maximal_Simplex_Vertex:
    _vertex_set: set[Eji] = field(default_factory=set)

    def check_valid(self):
        # every j index in the set must appear at most once
        j_vals = { eji.j for eji in self._vertex_set }
        assert len(j_vals) == len(self._vertex_set)

@dataclass
class Maximal_Simplex_Vertices:
    """These are stored in a list which is required to be ordered from big to small
    under the same ordering used to order eji's."""
    _vertex_list: list[Maximal_Simplex_Vertex]

    def to_Eji_ordering(self) -> Eji_Ordering:
        vertices_and_null = self._vertex_list + [Maximal_Simplex_Vertex()]
        simplex_eji_ordering = [(v1._vertex_set - v2._vertex_set).pop() for v1, v2 in pairwise(
            vertices_and_null)]  # The set c1-c2 should contain only one element, so pop() should return it.
        return Eji_Ordering(simplex_eji_ordering)

    def check_valid(self):
        """This function asserts all sorts of things that should be true for a valid object.
        Use it in unit-tests to raise assertion errors."""
        for v_larger, v_smaller in pairwise(self._vertex_list):
            v_larger.check_valid()
            v_smaller.check_valid()
            #print("LARGER SMALLER ",v_larger,v_smaller)
            gain = v_larger._vertex_set - v_smaller._vertex_set
            loss = v_smaller._vertex_set - v_larger._vertex_set
            assert len(gain) == 1, "Every vertex should have an Eji not contained in the next vertex."
            if loss:  # Something got deleted, so check that what was deleted grew in i
                assert len(loss) == 1
                for eji_loss in loss:
                    break
                for eji_gain in gain:
                    break
                assert eji_loss.j == eji_gain.j
                assert eji_loss.i + 1 == eji_gain.i
            if gain and not loss: # new j got added, so check that what was deleted grew started at base
                for eji_gain in gain:
                    break
                assert eji_gain.i == 0

#@dataclass
#class Maximal_Simplex:
#    """Class to hold any of the big simplices which (before barycentric subdivision)
#    form the beginnings of our simplicial complex.  It holds an eij_ordering."""
#    eji_ordering: Eji_Ordering
#    vertices: Maximal_Simplex_Vertices
#
#    def __init__(self, ):
#        pass

def ell(c, k, shrink=False):
    """
    The function ell(c, k) can (in principle) be anything that satisfies the properties listed below.
    In practice, presumably some choices are better than others for efficiency reasons or reasons of practicality.
    TODO: Therefore one should experiment with alternatives that go beyond the choices made here!

    INPUT REQUIREMENTS:
    * The input k shall be a non-negative integer
    * The input c shall be a (possibly empty) set of (j,i) pairs, with j in [0,n-1] and i in [0,k-1].
    * The set of j values in c shall have no repeates.  I.e. if there are three pairs in c then one pair will have j=0, one pair will have j=1 and one pair will have j=2.  [Aside: this restricts the length of c to be at most n.]

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
    assert k >= 0, "k should be a non-negative integer."
    len_c = len(c)
    assert len({ j for j,_ in c }) == len_c, "No j should repeat."

    #print("c was = ",c)

    i_vals_sorted_by_j_vals = [i for _,i in sorted(list(c)) ] # Fortunately j comes first in (j,i) so this will work.
    # Note that above we do not bother storing the j values as we know they will be 0,1,..,len(c)-1 given
    # the input preconditions.  Thus we will be done if we can hash i_vals_sorted_by_j_vals to a non-colliding value.
    # print("i_vals_sorted_by_j_vals = ",i_vals_sorted_by_j_vals)

    # Either of the two lines below should work identically. Just use one!
    # ell_value = sum(( i*(k**(len_c-1-pos))  for pos,i in enumerate(i_vals_sorted_by_j_vals) ))  +  sum((k**i for i in range(len_c)))
    ell_value_integer = sum(( i*(k**(len_c-1-pos)) + k**pos for pos,i in enumerate(i_vals_sorted_by_j_vals) ))

    # print("ell_value before nonlinear tfm= ",ell_value_integer)
    
    # At this point ell is an integer in 0,1,2,3,4,5, ...
    # We may wish to non-linearly transform it into (-pi/2,pi/2)
   
    if shrink:
        alternate_sign = 2*(ell_value_integer % 2)-1 # Will be +1 or -1 depending on even/oddness of ell_value_ingeger
        ell_value = ell_value_integer * alternate_sign
        ell_value = np.arctan(np.float64(ell_value)/50) # puts ell in (-pi/2,pi/2)
    else:
        ell_value = ell_value_integer

    return ell_value

def make_flat_sums(n,k,delta, sort=False, prepend_zero=False):
    """
    Conceptually, the dict flat_sums (for k=3) should "represent" the following map:
    
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

    However, for practical implementation purposes we "represent" the above by the following more abbreviated structure
    (a list of tuples)
    in which for each key the first index is j in [0,n-1], the second index is
    a tuple containing the i values in the basis sum,
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
    # print("flat_sums unsorted",flat_sums)
    if sort:
        flat_sums = sorted(flat_sums, key=lambda x : (x[2], len(x[1])) ) # Sort by delta sum, but break ties in favour of longer sums
        # print("flat_sums sorted",flat_sums)
    if prepend_zero:
        flat_sums = [ ( None, tuple(), 0) ] + flat_sums
    return flat_sums

def make_c_dc_pairs_n2k2(delta):
    # Each key in the "delta" dict is an (j,i) tuple representing Patrick's e^j_i with j in [0,n-1] and i in [0,k-1].  The associated value is the coefficient of that e^j_i basis vector in the associated element of (\Delta_k)^n.
    # e.g delta = {  
    #     (0,0) : 0.5, (0,1) : 0.2, (0,2) : 0.1,    #a point in the 1st simplex (simplex 0)
    #     (1,2) : 0.25,                             #a point in the 2nd simplex (simplex 1)
    #     (2,0) : 0.1,                              #a point in the 3rd simplex (simplex 2)
    #   }
    a=delta[(0,0)]
    b=delta[(0,1)]
    c=delta[(1,0)]
    d=delta[(1,1)]

    # TEST DONT!!!!!
    ### if a+b < max([b,c+d,d]):
    ###     # swap j=0 with j=1
    ###     a,b,c,d = c,d,a,b
    
    if c+d >=d >= a+b >= b: # C'
        simplex = "left"
        c_dc_pairs = [
            ({(0,1), (1,1)},       b),
            ({(0,0), (1,1)},       a),
            ({       (1,1)},   d-a-b),
            ({       (1,0)},       c),
            ]
    elif c+d >= a+b >= b >= d: # A'
        simplex = "left"
        c_dc_pairs = [
            ({(0,1), (1,1)},       d),
            ({(0,1), (1,0)},     b-d),
            ({(0,0), (1,0)},       a),
            ({       (1,0)}, c+d-a-b),
            ]
    elif c+d >= a+b >= d >= b: # B'
        simplex = "left"
        c_dc_pairs = [
            ({(0,1), (1,1)},       b),
            ({(0,0), (1,1)},     d-b),
            ({(0,0), (1,0)},   a+b-d),
            ({       (1,0)}, c+d-a-b),
            ]
    elif a+b >= c+d >= d >= b: # A
        simplex = "left"
        c_dc_pairs = [
            ({(0,1), (1,1)},       b),
            ({(0,0), (1,1)},     d-b),
            ({(0,0), (1,0)},       c),
            ({(0,0)},        a-c+b-d),
            ]
    elif a+b >= c+d >= b >= d: # B
        simplex = "mid"
        c_dc_pairs = [
            ({(0,1), (1,1)},       d),
            ({(0,1), (1,0)},     b-d),
            ({(0,0), (1,0)},   c+d-b),
            ({(0,0)},        a-c+b-d),
            ]
    elif a+b >= b >= c+d >= d: # C
        simplex = "right"
        c_dc_pairs = [
            ({(0,1), (1,1)},       d),
            ({(0,1), (1,0)},       c),
            ({(0,1)},          b-c-d),
            ({(0,0)},              a),
            ]
    else:
        simplex = None
        assert False

    return c_dc_pairs


    

def make_c_dc_pairs(n , k,  # Only need n and/or k if doing "original initialisation" of x_with_coeffs 
                    delta,
                    # Each key in the delta dict is an (j,i) tuple representing Patrick's e^j_i with j in [0,n-1] and
                    # i in [0,k-1].  The associated value is the coefficient of that e^j_i basis vector in the
                    # associated element of (\Delta_k)^n.
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
    """A set rather than a list is used to hold the coordinate vectors because later we want to find out 
    "elements in one set not in another" ... and so if we had used lists we would have to construct a set from a 
    list later anyway.  Fortunately the objects represented are sets anyway (they represent sums of dissimilar
     basis elements which are vertices, and sums are order independent).  The set creation comprehension does not 
     produce duplicate elements squashed by the set, though, so if it's later needed they could be changed back to a 
     list here (instead of set) so long as the later set-difference calculation is done some other way."""

    #print("c_dc_pairs from flat_sums = ")
    #[print(_) for _ in c_dc_pairs]

    return c_dc_pairs

def pr(r, big_n):
    # Method below makes negative numbers from positive integer r if r is big enough!  Floating point wrap around! Must make r real
    return np.power(np.float64(r), np.arange(big_n)) # Starting at zeroeth power so that r can be both zero and non-zero without constraint.

def map_Delta_k_to_the_n_to_c_l_dc_triples(n, k, delta : Position_within_Simplex_Product, use_n2k2=False):

    if use_n2k2 and n==2 and k==2:
        c_dc_pairs = make_c_dc_pairs_n2k2(delta)
    else:
        c_dc_pairs = make_c_dc_pairs(n,k,delta)
 
    ####TEST_REMOVE#### vertices = Maximal_Simplex_Vertices([ c for c,_ in c_dc_pairs ])
    ####TEST_REMOVE#### #print("vertices (before modding by S(n)) =")
    ####TEST_REMOVE#### #[ print(c) for c in vertices ]

    ####TEST_REMOVE#### """
    ####TEST_REMOVE#### The following simplex_eji_ordering contains the implied basis element ordering (greatest first)
    ####TEST_REMOVE#### which defined the simplex in which we the point delta stands.
    ####TEST_REMOVE#### """
    ####TEST_REMOVE#### simplex_eji_ordering = vertices.to_eji_ordering()
    ####TEST_REMOVE#### #print("simplex_eji_ordering (before mod S(n)) =")
    ####TEST_REMOVE#### #[ print(eji) for eji in simplex_eji_ordering ]

    ####TEST_REMOVE#### # We must canonicalise the simplex by detecting and modding out the relevant perm of S(n).


    ####TEST_REMOVE#### 
    ####TEST_REMOVE#### # First detect the perm needed to take our simplex to canonical form:
    ####TEST_REMOVE#### perm = make_perm_from_simplex(simplex_eji_ordering, from_right=True) # It is not critical whether we come from right or left, since any canonical form will do. I choose from_right as it matches the conventin I used in some OneNote nootbooks while I was getting to grips with things. from_left would be faster as no need to reverse a list internally.  Consider moving to from_left later.
    ####TEST_REMOVE#### #print("perm = ",perm)
    ####TEST_REMOVE#### 
    ####TEST_REMOVE#### # Actually we need the inverse perm!
    ####TEST_REMOVE#### inverse_perm = invert_perm(perm)
    ####TEST_REMOVE#### #print("inverse perm = ", inverse_perm)

    ####TEST_REMOVE#### # Don't actually need the next thing -- but compute it for debug purposes "just in case"
    ####TEST_REMOVE#### simplex_eji_ordering_after_mod_Sn = [ (inverse_perm[j], i) for (j,i) in simplex_eji_ordering ] 
    ####TEST_REMOVE#### #print("simplex_eji_ordering (after mod S(n)) =")
    ####TEST_REMOVE#### #[ print(eji) for eji in simplex_eji_ordering_after_mod_Sn ]

    ####TEST_REMOVE#### # Now 'canonicalise' the vertices in c_dc_pairs using that perm:
    ####TEST_REMOVE#### c_dc_pairs_after_mod_Sn = [ ({ (inverse_perm[j], i) for (j,i) in c }, dc)  for (c,dc) in c_dc_pairs   ]

    # TEST DON'T APPLY PERM!!!!! It was a mistake!!!!!
    c_dc_pairs_after_mod_Sn = c_dc_pairs

    #print("c_dc_pairs (after modding by S(n)) =")
    #[ print(c) for c in c_dc_pairs_after_mod_Sn ]
    
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
    point_in_R_bigN = sum([d * pr(ell, big_n) for _, ell, d in c_l_dc_triples]) + np.zeros(big_n)  # Addition of zero term at end ensures that we still get a zero vec (not 0) in the event that c_l_dc_triples is empty!

    return c_l_dc_triples, point_in_R_bigN 

def vector_to_simplex_point(vec):
    k = len(vec)
    vec = np.array(vec)
    return 1.0/(k*(1.0+np.power(2.0,vec))) # TODO: This somewhat crude parameterisation does not use the WHOLE of the simplex -- so it's a bit wasteful. It also has terrible dynamic range problems and even unit issues. Might want to address all of these points with a better mapping.

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
            raise Exception("Vectors supplied to vectors_to_delta are not all the same dimension!")
        for i in range(k):
            delta[(j,i)]=simplex_point[i]
    return delta


def make_perm_from_simplex(simplex_eji_ordering, from_right=False):
    # Note that setting from_right does not (in general) reverse the answer even though it reverses the input.
    # I.e. perm_from_right(ordering)[::-1] is not in general the same as perm_from_left(ordering[::-1]).
    if from_right:
      simplex_eji_ordering=simplex_eji_ordering[::-1]
    return list({ j[0] : None for j in simplex_eji_ordering  }) # Uses insertion order preservation

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
    def test1(self):
        vertices = Maximal_Simplex_Vertices([
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 2), Eji(2, 2), Eji(3, 2)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 1), Eji(2, 2), Eji(3, 2)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 1), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(1, 0), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 2), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 1), Eji(2, 2), Eji(3, 1)}),
            Maximal_Simplex_Vertex({Eji(0, 1), Eji(2, 2), Eji(3, 0)}),
            Maximal_Simplex_Vertex({Eji(0, 1), Eji(2, 2)}),
            Maximal_Simplex_Vertex({Eji(0, 0), Eji(2, 2)}),
            Maximal_Simplex_Vertex({Eji(2, 2)}),
            Maximal_Simplex_Vertex({Eji(2, 1)}),
            Maximal_Simplex_Vertex({Eji(2, 0)}),
        ])
        vertices.check_valid()

        ordering_calculated = vertices.to_Eji_ordering()

        ordering_expected = Eji_Ordering([
            Eji(1, 2),
            Eji(3, 2),
            Eji(1, 1),
            Eji(1, 0),
            Eji(0, 2),
            Eji(3, 1),
            Eji(3, 0),
            Eji(0, 1),
            Eji(0, 0),
            Eji(2, 2),
            Eji(2, 1),
            Eji(2, 0),
        ])
        ordering_expected.check_valid()

        self.assertEqual(ordering_calculated, ordering_expected)

class TestSimplexPositions(unittest.TestCase):
        def test_pos_within_simplex(self):
            aBad = Position_within_Simplex([2, 2, 3])
            self.assertRaises(Exception, aBad.check_valid)

            a = Position_within_Simplex([0.1, 0.25, 0.15])
            a.check_valid()

            b = Position_within_Simplex(np.array([0.5, 0.25, 0.25]))
            b.check_valid()
            self.assertEqual(b, Position_within_Simplex([0.5, 0.25, 0.25])) # Not using np.array

            c = Position_within_Simplex([1.0/3.0, 1.0/3.0, 1.0/3.0])
            c.check_valid()

            dBad = Position_within_Simplex([0, -0.23, 0])
            self.assertRaises(Exception, dBad.check_valid)

            big_1 = Position_within_Simplex_Product([b, c, a, a, b])
            big_1.check_valid()
            #big_1_0 = big_1[0]
            #print("Big_1[0] is ",big_1_0)
            #print("b        is ", b)
            self.assertEqual(big_1[0], b)
            self.assertEqual(big_1[1], c)
            self.assertEqual(big_1[2], a)
            self.assertEqual(big_1[3], a)
            self.assertEqual(big_1[4], b)

            big_2 = Position_within_Simplex_Product([[0.1, 0.2], [0.3, 0.11]])
            self.assertEqual(big_2[0], Position_within_Simplex([0.1, 0.2]))
            self.assertEqual(big_2[1], Position_within_Simplex([0.3, 0.11]))
            self.assertEqual(big_2[0, 0], 0.1)
            self.assertEqual(big_2[0, 1], 0.2)
            self.assertEqual(big_2[1, 0], 0.3)
            self.assertEqual(big_2[1, 1], 0.11)

            big_3 = Position_within_Simplex_Product([b, c, b, b, dBad])
            self.assertRaises(Exception, big_3.check_valid)

class Test_perm_detection(unittest.TestCase):
    def test(self):

        simplex_eji_ordering = [ (1, 2), (3, 2), (1, 1), (0, 2), (3, 1), (3, 0), (0, 1), (1, 0), (0, 0), (2, 2), (2, 1), (2, 0), ]

        simple_ordering_on_j_vals_from_left_expected = [ 1, 3, 0, 2 ] # j vals read from left, ignoring repeats
        simple_ordering_on_j_vals_from_right_expected = [ 2, 0, 1, 3 ] # j vals read from right, ignoring repeats

        ordering_from_left_calculated = make_perm_from_simplex(simplex_eji_ordering)
        ordering_from_right_calculated = make_perm_from_simplex(simplex_eji_ordering, from_right=True)

        self.assertEqual(simple_ordering_on_j_vals_from_left_expected, ordering_from_left_calculated)
        self.assertEqual(simple_ordering_on_j_vals_from_right_expected, ordering_from_right_calculated)

if __name__ == "__main__":
    test_simplex_embedding()
    unittest.main(exit=False)