# Encode list of real numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# Although this implementation claims to only do reals, it does in fact (privately) encode complex lists, albeit to complex outputs.


name="Cinf_numpy_polynomial_encoder_for_array_of_reals"

import numpy as np
import Cinf_numpy_polynomial_encoder_for_list_of_reals
import tools

def encode(data):

    n,m = data.shape
    print(f"Size (m,n)=({m},{n})")

    # We need to do different things depending on the shape of the input:

    if m==1:
        # The "vectors" are 1-long, so reduce the thing to a list.
        return Cinf_numpy_polynomial_encoder_for_list_of_reals.encode(data[:,0])

    if m==2:
        # The "vectors" are 2-long, so turn them into complex numbers, encode, and expand:
        complex_list = data[:,0]+complex(0,1)*data[:,1]
        complex_encoding = Cinf_numpy_polynomial_encoder_for_list_of_reals.encode(complex_list) # Yes, this is explopiting a secret private feature ...
        real_encoding = tools.expand_complex_to_real_pairs(complex_encoding)
        return real_encoding

    pass
