#!/usr/bin/env python

from collections.abc import Iterable
from fractions import Fraction
from itertools import pairwise
import numpy as np

from tools import numpy_array_of_frac_to_str

def pretty_print_lin_comb(lin_comb):
    for coeff, basis_elt in lin_comb:
        print(float(coeff), numpy_array_of_frac_to_str(basis_elt))

class MonoLinComb:
    def __init__(self, coeff, basis_vec):
        self.coeff = coeff
        self.basis_vec = basis_vec

class LinComb:
    def __init__(self):
        self.coeffs = []
        self.basis_vecs = []

    def __len__(self):
        assert len(self.coeffs) == len(self.basis_vecs)
        return len(self.coeffs)

    def __iadd__(self, stuff):
        print(f"In iadd see stuff of type {stuff}")
        # Note that __add__ does not consolidate. I.e. (3i+2j) + (5i) becomes (3i+2j+5i) not (8i+2j).
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
        basis_elts_as_tuptup = tuple(map(tuple, self.basis_elts))
        return len(set(basis_elts_as_tuptup)) == len(basis_elts_as_tuptup)

    def __str__(self):
        tmp = list(zip(self.coeffs, self.basis_vecs))
        return str(f"{tmp}")

def array_to_lin_comb(arr: np.array, debug=False):
        lin_comb = LinComb()
        for index, coeff in np.ndenumerate(arr):
            basis_vec = np.zeros_like(arr)
            basis_vec[index] = 1
            lin_comb += MonoLinComb(coeff, basis_vec)
        return lin_comb

def barycentric_subdivide(lin_comb: LinComb, return_offset_separately=False, debug=False):
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

    if self.preserve_scale:
        diff_lin_comb = LinComb(MonoLinComb((fac := (i+1))*(x-y), sum(basis_vecs[:i+1], start=0*basis_vecs[0]+Fraction())/fac) for i, (x,y) in enumerate(pairwise(coeffs)))
        offset_lin_comb = LinComb(MonoLinComb((fac := len(basis_vecs))*coeffs[-1], sum(basis_vecs, start=0*basis_vecs[0]+Fraction())/fac))
    else:
        diff_lin_comb = LinComb(MonoLinComb((x-y), sum(basis_vecs[:i+1], start=0*basis_vecs[0])) for i, (x,y) in enumerate(pairwise(coeffs)))
        offset_lin_comb = LinComb(MonoLinComb(coeffs[-1], sum(basis_vecs, start=0*basis_vecs[0])))

    if debug:
        print(f"diff_lin_comb is\n{diff_lin_comb}")
        print(f"offset_lin_comb is\n{offset_lin_comb}")

    if return_offset_separately:
        ans = diff_lin_comb, offset_lin_comb
    else:
        ans = diff_lin_comb + offset_lim_comb

    if debug:
        print(f"About to return \n{ans}")

    return ans

