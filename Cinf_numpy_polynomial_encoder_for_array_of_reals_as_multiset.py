# Encode array of real numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [[3,4],[4,2],[-2,1]]
#
# when used to represent this multiset {{ }}:
#
#        {{ [3,4],[4,2],[-2,1] }}
#
# total_encoding_size = m*(m-1)*n
#
# where n is the number of vectors in the multiset and m is their dimension. E.g in the example above m=2 and n=3.

import numpy as np
import Cinf_numpy_polynomial_encoder_for_list_of_reals_as_multiset
import itertools
import tools

def encode(data):

    n,m = data.shape
    #print(f"Size (m,n)=({m},{n})")

    # We need to do different things depending on the shape of the input:

    if m==1:
        # The "vectors" are 1-long, so reduce the thing to a list.
        return Cinf_numpy_polynomial_encoder_for_list_of_reals_as_multiset.encode(data[:,0])

    if m==2:
        # The "vectors" are 2-long, so turn them into complex numbers, encode, and expand:
        complex_list = data[:,0]+complex(0,1)*data[:,1]
        complex_encoding = Cinf_numpy_polynomial_encoder_for_list_of_reals_as_multiset.encode(complex_list) # Yes, this is explopiting a secret private feature ...
        real_encoding = tools.expand_complex_to_real_pairs(complex_encoding)
        return real_encoding

    # The "vectors" are 3-or-more-long, so need to take all m-choose-2 pairings of elements in them, and send them out.
    # We can use the m==2 case code above for that.
    number_of_pairs = m*(m-1)//2
    # pair_encoding_size = 2*n 
    # total_encoding_size = m*(m-1)*n
    current_encoding_index = 0 
    for row1_index, row2_index in itertools.combinations(range(m), 2):
        pair_of_rows = data[:,[row1_index, row2_index]]
        #print("About to request coding for",pair_of_rows)
        encoding_for_pair = encode(pair_of_rows)
        if current_encoding_index == 0:
            # Allocate array of appropriate type for all the pairs that will come later:
            # Get encoding size.  This SHOULD be 2*n but safer to get from data for future proofing
            pair_encoding_size = len(encoding_for_pair)
            #print("pes",pair_encoding_size,"nop",number_of_pairs)
            total_encoding_size = pair_encoding_size * number_of_pairs
            real_encoding = np.empty(total_encoding_size, dtype = encoding_for_pair.dtype)
        real_encoding[current_encoding_index:current_encoding_index+pair_encoding_size] = encoding_for_pair
        current_encoding_index += pair_encoding_size
    return real_encoding

