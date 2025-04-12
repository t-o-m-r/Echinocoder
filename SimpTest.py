#!/usr/bin/env python

import EncDec
import numpy as np
from itertools import pairwise
import sys

def print_simplex_1_bit(set_array : np.array,
             preserve_scale_in_step_1 = False,
             preserve_scale_in_step_2 = False):
    simplex_1_bit = EncDec.Chain([
        EncDec.ArrayToLinComb(input_array_name="set", output_lin_comb_name="lin_comb_0"),
        EncDec.BarycentricSubdivide("lin_comb_0", "lin_comb_1_first_diffs", "offset", preserve_scale=False),
        EncDec.BarycentricSubdivide("lin_comb_1_first_diffs", "lin_comb_2_second_diffs",
                             "lin_comb_2_second_diffs", pass_forward="offset", pass_backward="offset", preserve_scale=False),
        EncDec.MergeLinCombs(["lin_comb_2_second_diffs", "offset"], "lin_comb_3"),
    ])

    input_dict = { "set" : set_array, }

    enc = simplex_1_bit.encode(input_dict, debug=False)
    print(f"=======================\nSimplex1 as a chain encoded")
    print(EncDec.numpy_array_of_frac_to_str(input_dict["set"]))
    print("to")
    #print(f"{enc}")

    lin_comb_3 = enc["lin_comb_3"]
    #print(f"Note that lin_comb_3 is")
    EncDec.pretty_print_lin_comb(lin_comb_3)
    print("and the (non-offset) differences are")
    [ print(EncDec.numpy_array_of_frac_to_str(tmp:=b-a), " with ", np.sum(tmp)," ones in it") for a,b in list(pairwise( [a for _,a in lin_comb_3 ]))[:-1] ]


def loc(the_list, query):
    for i, entry in enumerate(the_list):
        if entry == query:
            return i
    return None

if __name__ == "__main__":
    #print_simplex_1_bit(np.asarray([[2,3],[4,7]]) )
    #print_simplex_1_bit(np.array(eval("[[2,3],[4,7]]")) )

    # Defaults:
    arr = np.array([[2,3,4], [4,7,1], [3,-2,1], [9,8,2]])

    # Override defaults:
    if (l := loc(sys.argv, "array")) is not None and l+1 < len(sys.argv): 
        arr = np.array(eval(sys.argv[l+1]))
    
    n, k = arr.shape

    if (l := loc(sys.argv, "n")) is not None and l+1 < len(sys.argv): 
        n = int(sys.argv[l+1])
    if (l := loc(sys.argv, "k")) is not None and l+1 < len(sys.argv): 
        k = int(sys.argv[l+1])

    randomise_array = "random" in sys.argv
    if randomise_array:
         print (f"n is {n} and k is {k}")
         arr = np.random.randint(low=-9, high=30, size=(n,k))

    print_simplex_1_bit(arr)
    

