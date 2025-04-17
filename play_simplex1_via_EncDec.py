#!/usr/bin/env python

import EncDec
import numpy as np
from itertools import pairwise
import sys
import tools


def print_first_part_of_simplex_1_encoding(set_array : np.array,
             preserve_scale_in_step_1 = False,
             preserve_scale_in_step_2 = False):

    """
    Step 1: 

    Turn the array (which represents a set) into a linear combination of coefficients and Eji basis elements.
    Conceptually this is turning:

       set_array = [[2,8],[4,5]]

    into

       lin_comb_0 = 2 * [[1,0],[0,0]] + 8 * [[0,1],[0,0]] + 4 * [[0,0],[1,0]] + 5 * [[0,0],[0,1]]

    """
    lin_comb_0 = EncDec.array_to_lin_comb(set_array)


    """
    Step 2:

    Re-write lin_comb_0 as a sum of the offset (which is the minimum coefficient times [[1,1],[1,1]] and some
    (so called) differences.  The latter are a set of non-negative coefficients times other basis vectors only 
    containing zeros and ones.  Conceptually this step is turning:

       lin_comb_0 = 2 * [[1,0],[0,0]] + 8 * [[0,1],[0,0]] + 4 * [[0,0],[1,0]] + 5 * [[0,0],[0,1]]

    into

       lin_comb_1 + offset

    where the first differences are:
    
        lin_comb_1 = (8-5) * [[0,1],[0,0]]
                   + (5-4) * [[0,1],[0,1]]  
                   + (4-2) * [[0,1],[1,1]] 

    and where the offset is:

        offset = 2 * [[1,1],[1,1]]

    The above example assumed that preserve_scale=False is supplied to barycentric_subdivide, and that thus
    the one-norm of the basis vecs in the linear combination is growing as you go down the list, rather than
    constant as it would be if preserve_scale=True had been used instead.
    """
    lin_comb_1_first_diffs, offset = EncDec.barycentric_subdivide(lin_comb_0, return_offset_separately=True, preserve_scale=preserve_scale_in_step_1)


    lin_comb_2_second_diffs = EncDec.barycentric_subdivide(lin_comb_1_first_diffs, return_offset_separately=False, preserve_scale=preserve_scale_in_step_2)
    lin_comb_3 = EncDec.LinComb( (lin_comb_2_second_diffs, offset) )

    print(f"=======================\nSimplex1 as a chain encoded")
    print(EncDec.numpy_array_of_frac_to_str(set_array))
    print("to")
    EncDec.pretty_print_lin_comb(lin_comb_3)
    print("the first is")
    print(EncDec.numpy_array_of_frac_to_str(tmp:=lin_comb_3.basis_vecs[0]), " with ", np.sum(tmp), " ones in it")
    print("and the (non-offset) differences are")
    [ print(EncDec.numpy_array_of_frac_to_str(tmp:=b-a), " with ", np.sum(tmp)," ones in it") for a,b in list(pairwise( lin_comb_3.basis_vecs ))[:-1] ]

    print("----- Canonicalised lin enc: -----")
    can_lin_comb_3 = EncDec.LinComb([ EncDec.MonoLinComb(coeff, tools.sort_np_array_rows_lexicographically(arr)) for coeff, arr in zip(lin_comb_3.coeffs, lin_comb_3.basis_vecs) ])

    EncDec.pretty_print_lin_comb(can_lin_comb_3)
    print("the first is")
    print(EncDec.numpy_array_of_frac_to_str(tmp:=can_lin_comb_3.basis_vecs[0]), " with ", np.sum(tmp), " ones in it")
    print("and the (non-offset) differences are")
    [ print(EncDec.numpy_array_of_frac_to_str(tmp:=b-a), " with ", np.sum(tmp)," ones in it") for a,b in list(pairwise(  can_lin_comb_3.basis_vecs ))[:-1] ]




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
    

