#!/usr/bin/env python

from collections.abc import Iterable
from fractions import Fraction
from itertools import pairwise
import numpy as np

from tools import numpy_array_of_frac_to_str

class MonoLinComb:
    def __init__(self, coeff, basis_vec):
        self.coeff = coeff
        self.basis_vec = basis_vec

    def __repr__(self):
        return f"MonoLinComb({repr(self.coeff)}, {repr(self.basis_vec)})"

    def __eq__(self, other):
        return self.coeff == other.coeff and np.array_equal(self.basis_vec, other.basis_vec)

class LinComb:
    def __init__(self, initialiser=None):
        self.coeffs = []
        self.basis_vecs = []
        if initialiser is not None:
            self += initialiser

    def mlcs(self): # MLCS = Mono Lin CombinationS
        return (MonoLinComb(c,b) for c,b in zip(self.coeffs, self.basis_vecs))

    def __len__(self):
        assert len(self.coeffs) == len(self.basis_vecs)
        return len(self.coeffs)

    def to_numpy_array(self):
        ans = None
        first = True
        for c,b in zip(self.coeffs, self.basis_vecs):
            if first == True:
                ans = c*np.asarray(b)
                first = False
            else:
                ans += c*np.asarray(b)
        return ans

    def __add__(self, stuff):
        return LinComb((self, stuff))

    def __iadd__(self, stuff):
        #print(f"In iadd see stuff of type {stuff}")
        # Note that __add__ does not automatically consolidate. I.e. (3i+2j) + (5i) becomes (3i+2j+5i) not (8i+2j).
        # It is the user's responsibility to perform consolidation manually if they wish it to happen!!
        if isinstance(stuff, LinComb):
            self.coeffs.extend(stuff.coeffs)
            self.basis_vecs.extend(stuff.basis_vecs)
            return self

        if isinstance(stuff, MonoLinComb):
            self.coeffs.append(stuff.coeff)
            self.basis_vecs.append(stuff.basis_vec)
            return self

        if isinstance(stuff, Iterable):
            for elt in stuff:
                self += elt # Recurse!
            return self
        
        print(f"DDDD {stuff}")
        raise ValueError("LinComb.__iadd__ only knows how to add LimCombs and MonoLinCombs and iterables containing those.")

    def is_consolidated(self):
        print(f"Being asked for consolidation state of {self.basis_vecs}")
        # Need to convert 2D arrays to tup(tup()) and 1D arrays to tup() so that they are hashable:
        basis_vecs_as_tuptups = [ (tuple(map(tuple, bv)) if bv.ndim == 2 else tuple(bv)) for bv in self.basis_vecs ]
        print(f"turned {self.basis_vecs} into {basis_vecs_as_tuptups}")
        return len(set(basis_vecs_as_tuptups)) == len(basis_vecs_as_tuptups)

    def __repr__(self):
        tmp = list(MonoLinComb(c,np.asarray(b)) for c,b in zip(self.coeffs, self.basis_vecs))
        return str(f"LinComb({tmp})")

    def __eq__(self, other):
        if len(self.coeffs) != len(other.coeffs):
            print("Found differing length")
            return false

        assert len(self.coeffs) == len(self.basis_vecs)
        assert len(other.coeffs) == len(other.basis_vecs)

        # Note that the order is required to match here, so eq means "same lin com in same order".
        for i,j in zip(self.mlcs(), other.mlcs()):
            if i != j:
               print("Found differing mlc")
               return False

        return True

def array_to_lin_comb(arr: np.array, debug=False):
        lin_comb = LinComb()
        for index, coeff in np.ndenumerate(arr):
            basis_vec = np.zeros_like(arr)
            basis_vec[index] = 1
            lin_comb += MonoLinComb(coeff, basis_vec)
        return lin_comb

def barycentric_subdivide(lin_comb: LinComb, return_offset_separately=False, preserve_scale=True, debug=False):
    """
        * If preserve_scale is True (default) then the sum of the coeffiencients is preserved. Equivalently, the one
          norm of each basis vector iw preserved at 1 if already at 1.
    """
    
    if debug:
        print(f"lin_comb is\n{lin_comb}")

    if len(lin_comb) == 0:
        return LinComb()

    assert len(lin_comb) >= 1

    assert lin_comb.is_consolidated() # Note that LinComb does not consolidate elements, but our use case should only encounter conslolidated elements anyway! Or so we think. If that is not so, we need to know about it here!

    # Sort by coefficient in linear combination, big -> small
    # We need a list below as we will consume it twice when generating the diff_lin_comb
    sorted_lin_comb = sorted(zip(lin_comb.coeffs, lin_comb.basis_vecs), key=lambda x: x[0], reverse=True)

    if debug:
        print(f"sorted_lin_comb is\n{sorted_lin_comb}")

    coeffs = [ x for x, _ in sorted_lin_comb ]
    basis_vecs = [ x for _ , x in sorted_lin_comb ]

    if preserve_scale:
        diff_lin_comb = LinComb(MonoLinComb((fac := (i+1))*(x-y), sum(basis_vecs[:i+1], start=0*basis_vecs[0]+Fraction())/fac) for i, (x,y) in enumerate(pairwise(coeffs)))
        offset_mono_lin_comb = MonoLinComb((fac := len(basis_vecs))*coeffs[-1], sum(basis_vecs, start=0*basis_vecs[0]+Fraction())/fac)
    else:
        diff_lin_comb = LinComb(MonoLinComb((x-y), sum(basis_vecs[:i+1], start=0*basis_vecs[0])) for i, (x,y) in enumerate(pairwise(coeffs)))
        offset_mono_lin_comb = MonoLinComb(coeffs[-1], sum(basis_vecs, start=0*basis_vecs[0]))

    if debug:
        print(f"diff_lin_comb is\n{diff_lin_comb}")
        print(f"offset_mono_lin_comb is\n{offset_mono_lin_comb}")

    if return_offset_separately:
        ans = diff_lin_comb, offset_mono_lin_comb
    else:
        ans = diff_lin_comb + offset_mono_lin_comb

    if debug:
        print(f"About to return \n{ans}")

    return ans

def pretty_print_lin_comb(lin_comb: LinComb):
    for coeff, basis_elt in zip(lin_comb.coeffs, lin_comb.basis_vecs):
        print(float(coeff), numpy_array_of_frac_to_str(basis_elt))

