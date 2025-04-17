#!/usr/bin/env python

import EncDec
import numpy as np
from itertools import pairwise
import sys
import tools

def pretty_print_lin_comb(lin_comb: EncDec.LinComb):
    for coeff, basis_elt in zip(lin_comb.coeffs, lin_comb.basis_vecs):
        print(float(coeff), tools.numpy_array_of_frac_to_str(basis_elt), " one-norm: ", np.sum(basis_elt))

def print_first_part_of_simplex_1_encoding(set_array : np.array,
                                           preserve_scale_in_step_1 = False,
                                           preserve_scale_in_step_2 = False):

    lin_comb_2_second_diffs, offset = EncDec.simplex_1_preprocess_steps(set_array,
                                                                        preserve_scale_in_step_1 = preserve_scale_in_step_1,
                                                                        preserve_scale_in_step_2 = preserve_scale_in_step_2,
                                                                        canonicalise = False,
                                                                        use_assertions = True)

    lin_comb_3 = lin_comb_2_second_diffs + offset

    print(f"=======================\nSimplex1 as a chain encoded")
    print(EncDec.numpy_array_of_frac_to_str(set_array))
    print("to")
    pretty_print_lin_comb(lin_comb_3)
    print("the first is")
    print(EncDec.numpy_array_of_frac_to_str(tmp:=lin_comb_3.basis_vecs[0]), " with basis one-norm ", np.sum(tmp))
    print("and the (non-offset) differences are")
    [ print(EncDec.numpy_array_of_frac_to_str(tmp:=b-a), " with basis one-norm ", np.sum(tmp)) for a,b in list(pairwise( lin_comb_3.basis_vecs ))[:-1] ]

    print("----- Canonicalised lin enc: -----")
    can_lin_comb_2_second_diffs, offset2 = EncDec.simplex_1_preprocess_steps(set_array,
                                                                             preserve_scale_in_step_1 = preserve_scale_in_step_1,
                                                                             preserve_scale_in_step_2 = preserve_scale_in_step_2,
                                                                             canonicalise = True,
                                                                             use_assertions = True)
    assert offset == offset2

    can_lin_comb_3 = can_lin_comb_2_second_diffs + offset2
    
    pretty_print_lin_comb(can_lin_comb_3)
    print("the first is")
    print(EncDec.numpy_array_of_frac_to_str(tmp:=can_lin_comb_3.basis_vecs[0]), " with basis one-norm", np.sum(tmp))
    print("and the (non-offset) differences are")
    [ print(EncDec.numpy_array_of_frac_to_str(tmp:=b-a), " with basis one-norm", np.sum(tmp)) for a,b in list(pairwise(  can_lin_comb_3.basis_vecs ))[:-1] ]




def loc(the_list, query):
    for i, entry in enumerate(the_list):
        if entry == query:
            return i
    return None

if __name__ == "__main__":
    #print_first_part_of_simplex_1_encoding(np.asarray([[2,3],[4,7]]) )
    #print_first_part_of_simplex_1_encoding(np.array(eval("[[2,3],[4,7]]")) )

    # Defaults:
    arr = np.array([[2,3,4], [4,7,1], [3,-2,1], [9,8,2]])
    preserve_scale_in_step_1 = False
    preserve_scale_in_step_2 = False


    # Override defaults:
    if (l := loc(sys.argv, "array")) is not None and l+1 < len(sys.argv): 
        arr = np.array(eval(sys.argv[l+1]))
    
    
    low=9
    high=30

    n, k = arr.shape

    if (l := loc(sys.argv, "n")) is not None and l+1 < len(sys.argv): 
        n = int(sys.argv[l+1])
    if (l := loc(sys.argv, "k")) is not None and l+1 < len(sys.argv): 
        k = int(sys.argv[l+1])
    if (l := loc(sys.argv, "low")) is not None and l+1 < len(sys.argv): 
        low = int(sys.argv[l+1])
    if (l := loc(sys.argv, "high")) is not None and l+1 < len(sys.argv): 
        high = int(sys.argv[l+1])
    if (l := loc(sys.argv, "scales")) is not None and l+2 < len(sys.argv):
        preserve_scale_in_step_1 = bool(int(sys.argv[l+1]))
        preserve_scale_in_step_2 = bool(int(sys.argv[l+2]))
    
    randomise_array = "random" in sys.argv
    if randomise_array:
         print (f"n is {n} and k is {k}")
         arr = np.random.randint(low=low, high=high, size=(n,k))

    print_first_part_of_simplex_1_encoding(arr, preserve_scale_in_step_1=preserve_scale_in_step_1, preserve_scale_in_step_2=preserve_scale_in_step_2)
    

