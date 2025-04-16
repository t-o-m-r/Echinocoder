#!/usr/bin/env python
from fractions import Fraction
from itertools import pairwise
import numpy as np

from tools import numpy_array_of_frac_to_str

def pretty_print_lin_comb(lin_comb):
    for coeff, basis_elt in lin_comb:
        print(float(coeff), numpy_array_of_frac_to_str(basis_elt))

class LinComb:
    def __init__(self):
        self.coeffs=[]
        self.basis_vecs=[]

    def __iadd__(self, stuff):
        print(f"In iadd see stuff of type {stuff}")
        # Note that __add__ does not consolidate. I.e. (3i+2j) + (5i) becomes (3i+2j+5i) not (8i+2j)
        if isinstance(stuff, LinComb):
            self.coeffs.extend(stuff.coeffs)
            self.basis_vecs.extend(stuff.basis_vecs)
            return self

        if isinstance(stuff, tuple) and len(stuff)==2:
            # Assume this:
            coeff, basis_vec = stuff
            self.coeffs.append(coeff)
            self.basis_vecs.append(basis_vec)
            return self

        raise ValueError("LinComb.__add__ only knows how to add LimCombs and coeff,basis_vec pairs.")

    def __str__(self):
        tmp = list(zip(self.coeffs, self.basis_vecs))
        return str(f"{tmp}")

def ArrayToLinComb(arr: np.array, debug=False):

        lin_comb = LinComb()
        for index, coeff in np.ndenumerate(arr):
            basis_vec = np.zeros_like(arr)
            basis_vec[index] = 1
            lin_comb += coeff, basis_vec

        return lin_comb

class Chain:
    def __init__(self, encoder_decoder_list):
        self.encoder_decoder_list = encoder_decoder_list

    def encode(self, input_dict, debug=False):
        for encoder in self.encoder_decoder_list:
            if debug:
                print(f"Chain is about to run {encoder.__class__}")
            input_dict = encoder.encode(input_dict, debug=debug)
        return input_dict

    def decode(self, output_dict, debug=False):
        for encoder in reversed(self.encoder_decoder_list):
            output_dict = encoder.encode(output_dict, debug=debug)
        return output_dict


class BarycentricSubdivide:
    """
    Encoding:
        * looks for a dictionary entry named self.input_name which is assumed to be a point in barycentric coordinates,
          i.e. a linear combination of basis element representing the vertices of a simplex,
        * calculates how this poing would be expressed ith respect to a different basis corresponding to a barycentric
          subdivision of the simplex,
        * creates a dictionary with an entry for self.output_name carrying the resulting linear combination, and
        * if "pass_through" is true, the encoder (and decode) will pass through all other elements of the input
          dictionary which do not result in overwriting of one of lin comb output.
        * If preserve_scale is True (default) then the sum of the coeffiencients is preserved. Equivalently, the one
          norm of each basis vector iw preserved at 1 if already at 1.

        A linear combination is assumed to be represented as a list of pairs -- with the first element of each pair
        being the coefficient and the second element of each pair being the corresponding basis verctor. I.e.
        [ (2, ei), (1, ej), (3, ek)]
        might represent the vector (2,1,3) with respect to the usual cartesian basis.

    Decoding:
        Reverse of encoding.
    """
    def __init__(self, input_name, diff_output_name, offset_output_name, pass_forward=None, pass_backward=None, preserve_scale=True):
        """

        Args:
            input_name: name of lin-comb to encode.
            diff_output_name: name of lin-comb into which to encode everything EXCEPT the constant offset term.
                               This lin-comb has only non-negative coefficients.
            offset_output_name: name of the lin-comb to encode the constant offset term.
                                This lin-comb may have coefficients of any sign.
            pass_through: whether or not to pass metadata in the input to the output (or vice versa).
                          If True, then pass everything through.
                          If False, then pass nothing through.
                          If list, then pass through dict items whose names are in the list

        """
        
        super().__init__(pass_forward, pass_backward)
        self.input_name = input_name
        self.diff_output_name = diff_output_name
        self.offset_output_name = offset_output_name
        self.common_output_name = diff_output_name if diff_output_name==offset_output_name else None
        self.preserve_scale = preserve_scale


    def encode(self, input_dict, pass_through=None, debug=False):
        if debug:
            print(f"input_dict is\n{input_dict}")

        output_dict = self.get_default_output_dict(input_dict, debug)

        if not self.input_name in input_dict:
            raise ValueError(f"Expected {self.input_name} in {input_dict}.")

        input_lin_comb = input_dict[self.input_name]
        """
        A linear combination is assumed to be represented as a list of pairs -- with the first element of each pair
        being the coefficient and the second element of each pair being the corresponding basis vector. I.e.
        [ (2, "i"), (1, "j"), (3, "k")]
        might represent the vector (2,1,3) with respect to the usual cartesian basis.
        """
        if debug:
            print(f"input_lin_comb is\n{input_lin_comb}")

        if not input_lin_comb:
            # List for p is empty, so
            if self.common_output_name:
                output_dict[self.common_output_name] = list()
            else:
                output_dict[self.diff_output_name] = list()
                output_dict[self.offset_output_name] = list()

            if debug:
                print(f"About to return \n{output_dict}")
            return output_dict

        assert len(input_lin_comb) >= 1

        # Sort by coefficient in linear combination, big -> small
        # We need a list below as we will consume it twice when generating the diff_lin_comb
        sorted_lin_comb = sorted(input_lin_comb, key=lambda x: x[0], reverse=True)
        if debug:
            print(f"sorted_lin_comb is\n{sorted_lin_comb}")

        coeffs = [ x for x, _ in sorted_lin_comb ]
        basis_vecs = [x for _ , x in sorted_lin_comb]

        """
        class ZeroObject(object):
            def __add__(self, other):
                return other
        """

        if self.preserve_scale:
            diff_lin_comb = list(((fac := (i+1))*(x-y), sum(basis_vecs[:i+1], start=0*basis_vecs[0]+Fraction())/fac) for i, (x,y) in enumerate(pairwise(coeffs)))
            offset_lin_comb = [((fac := len(basis_vecs))*coeffs[-1], sum(basis_vecs, start=0*basis_vecs[0]+Fraction())/fac)]
        else:
            diff_lin_comb = list(((x-y), sum(basis_vecs[:i+1], start=0*basis_vecs[0])) for i, (x,y) in enumerate(pairwise(coeffs)))
            offset_lin_comb = [(coeffs[-1], sum(basis_vecs, start=0*basis_vecs[0]))]

        if debug:
            print(f"diff_lin_comb is\n{diff_lin_comb}")
            print(f"offset_lin_comb is\n{offset_lin_comb}")

        if self.common_output_name:
            output_dict[self.common_output_name] = diff_lin_comb + offset_lin_comb
        else:
            output_dict[self.diff_output_name] = diff_lin_comb
            output_dict[self.offset_output_name] = offset_lin_comb
        if debug:
            print(f"About to return \n{output_dict}")

        return output_dict

