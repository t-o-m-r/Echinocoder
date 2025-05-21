#!/usr/bin/env python

import EncDec
import numpy as np
from itertools import pairwise
import sys
import tools
from Eji_LinComb import Eji_LinComb # For legacy regress code only

def pretty_print_lin_comb(lin_comb: EncDec.LinComb):
    for coeff, basis_elt in zip(lin_comb.coeffs, lin_comb.basis_vecs):
        print(" + ", float(coeff), "*", tools.numpy_array_of_frac_to_str(basis_elt), f" (index sum {np.sum(basis_elt)})")

def print_first_part_of_simplex_encoding(set_array : np.array,
                                         simplex_method = EncDec.simplex_1_embed,
                                         preserve_scale_in_step_1 = False,
                                         preserve_scale_in_step_2 = False,
                                         canonicalise = True,
                                         md5_step = False,
                                         debug = False):

    simplex_preprocess_steps = simplex_method.preprocess_steps

    lin_comb_2_second_diffs, offsets = simplex_preprocess_steps(set_array,
                                                                preserve_scale_in_step_1 = preserve_scale_in_step_1,
                                                                preserve_scale_in_step_2 = preserve_scale_in_step_2,
                                                                canonicalise = canonicalise,
                                                                use_assertions = True,
                                                                debug = debug)

    lin_comb_3 = lin_comb_2_second_diffs + offsets

    print(f"=======================\n{simplex_method} encoded")
    print(EncDec.numpy_array_of_frac_to_str(set_array))
    print(f"{'with' if canonicalise else 'without'} canonicalisation to second diff(s) ")
    pretty_print_lin_comb(lin_comb_2_second_diffs)
    print("and offset(s)")
    pretty_print_lin_comb(EncDec.LinComb(offsets))
    print("========================")
    if len(lin_comb_2_second_diffs)>=1:
        print("The first diff basis vector in the above is")
        print(EncDec.numpy_array_of_frac_to_str(tmp:=lin_comb_2_second_diffs.basis_vecs[0]), " with one-norm ", np.sum(tmp))
    if len(lin_comb_2_second_diffs)>=2:
        print("and the differences between the subsequent (non-offset) basis vectors are:")
        [ print(EncDec.numpy_array_of_frac_to_str(tmp:=b-a), " with one-norm ", np.sum(tmp)) for a,b in list(pairwise( lin_comb_2_second_diffs.basis_vecs )) ]

    if md5_step:
        print("========================")
        print("Trying to regenerate old MD5 output")
        if preserve_scale_in_step_1 != False or preserve_scale_in_step_2 != True:
            raise "Old MD5 output assumed normalisation of second barycentric subdivision and not of first."

        #difference_point_triples_tmp =  [  (index, coeff, basis_vecs) for index, (coeff, basis_vecs) in enumerate(zip(lin_comb_2_second_diffs.coeffs, lin_comb_2_second_diffs.basis_vecs)) ]
        #print("Made difference point triples:")
        #for dpt in difference_point_triples_tmp:
        #    print(dpt)

        difference_point_pairs =  [  (coeff, 
        #basis_vec 
        Eji_LinComb(0, 0)._setup_debug(index+1, (index+1)*basis_vec)
        ) for index, (coeff, basis_vec) in enumerate(zip(lin_comb_2_second_diffs.coeffs, lin_comb_2_second_diffs.basis_vecs)) ]
        print("Made difference point pairs:")
        for dpp in difference_point_pairs:
            print(dpp)









def loc(the_list, query):
    for i, entry in enumerate(the_list):
        if entry == query:
            return i
    return None

if __name__ == "__main__":

    # Defaults:
    arr = np.array([[2,3,4], [4,7,1], [3,-2,1], [9,8,2]])
    preserve_scale_in_step_1 = False
    preserve_scale_in_step_2 = False
    simplex_method = EncDec.simplex_1_embed

    # Override defaults:
    if (l := loc(sys.argv, "array")) is not None and l+1 < len(sys.argv): 
        arr = np.array(eval(sys.argv[l+1]))
    
    low=9
    high=30

    n, k = arr.shape

    md5_step = False

    if (l := loc(sys.argv, "n")) is not None and l+1 < len(sys.argv): 
        n = int(sys.argv[l+1])
    if (l := loc(sys.argv, "k")) is not None and l+1 < len(sys.argv): 
        k = int(sys.argv[l+1])
    if (l := loc(sys.argv, "low")) is not None and l+1 < len(sys.argv): 
        low = int(sys.argv[l+1])
    if (l := loc(sys.argv, "high")) is not None and l+1 < len(sys.argv): 
        high = int(sys.argv[l+1])
    if (l := loc(sys.argv, "method")) is not None and l+1 < len(sys.argv): 
        tmp = int(sys.argv[l+1])
        if tmp==1:
            simplex_method = EncDec.simplex_1_embed
        elif tmp==2:
            simplex_method = EncDec.simplex_2_embed
        else:
            raise ValueError(f"Don't know method {tmp}. Only know methods 1 and 2.")
            
    if "reproduce_old_injection" in sys.argv:
        preserve_scale_in_step_1 = False
        preserve_scale_in_step_2 = True
        md5_step = True

    if (l := loc(sys.argv, "scales")) is not None and l+2 < len(sys.argv):
        preserve_scale_in_step_1 = bool(int(sys.argv[l+1]))
        preserve_scale_in_step_2 = bool(int(sys.argv[l+2]))
  
    randomise_array = "random" in sys.argv
    if randomise_array:
         #print (f"n is {n} and k is {k}")
         arr = np.random.randint(low=low, high=high, size=(n,k))
   
    print()
    for canonicalise in (False, True):
        print(f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX{simplex_method}")
        print(dir(simplex_method))
        """ Shows ['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', 
        '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
        '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', 
        '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', 
        '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
        '__str__', '__subclasshook__', '__type_params__', 'postprocess_steps', 'preprocess_steps']
"""
        print(dir(simplex_method.preprocess_steps))
        """ Shows ['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', 
        '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
        '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', 
        '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', 
        '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
        '__str__', '__subclasshook__', '__type_params__']
"""

        print_first_part_of_simplex_encoding(arr, simplex_method=simplex_method.preprocess_steps,  canonicalise=canonicalise, preserve_scale_in_step_1=preserve_scale_in_step_1, preserve_scale_in_step_2=preserve_scale_in_step_2, md5_step=md5_step)
        """ Generates error message:
        
  Traceback (most recent call last):
  File "/Users/lester/github/Echinocoder/./play_simplex_encoders_via_EncDec.py", line 136, in <module>
    print_first_part_of_simplex_encoding(arr, simplex_method=(simplex_method.preprocess_steps),  canonicalise=canonicalise, preserve_scale_in_step_1=preserve_scale_in_step_1, preserve_scale_in_step_2=preserve_scale_in_step_2, md5_step=md5_step)
  File "/Users/lester/github/Echinocoder/./play_simplex_encoders_via_EncDec.py", line 22, in print_first_part_of_simplex_encoding
    simplex_preprocess_steps = simplex_method.preprocess_steps
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'function' object has no attribute 'preprocess_steps'
"""

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print()

    encoding = simplex_method(arr, preserve_scale_in_step_1=preserve_scale_in_step_1, preserve_scale_in_step_2=preserve_scale_in_step_2)

    print("Encoding was")
    for val in encoding:
        print(val)

    

