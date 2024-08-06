# Encode list of n real numbers treated as an element of a realprojectiveplane.
#
# This particular implentation explots a complex trick which (when n is even and greater than 0) allows the encoding save one real number over that required by trhe underlying regular implementation.
#
# I.e. the method encodes to:
#
#       0 reals when n is 0
#       2n-2 reals when n is even and n>0     (A SAVING OF ONE REAL!!)
#       2n-1 reals when n is odd.
#
# E.g. this method can encode an ordered list like this
#
#        x = [3,4,-2,5]
#
# which is deemed to be equivalent to its negation:
#
#        -x = [-3,-4,2,-5].
#
#

import numpy as np
import Cinf_python_regular_encoder_for_list_of_realsOrComplex_as_realOrComplexprojectiveplane as underlying_encoder

def encode(data):
    # data=np.asarray(data)
    return np.asarray([ np.trace(np.flipud(np.outer(data,data)),diag) for diag in range(1-len(data),len(data)) ])
    
# Just for testing/debug:
if __name__ == "__main__":
    data=[3,4,-2,5]
    #data=[3+2j,4,-2,5-4j]
    #data=[3+2j,4+1j,-2,5-4j]
    npd = np.asarray(data)
    outer = np.flipud(np.outer(npd, npd))
    traces = [ np.trace(outer,diag) for diag in range(1-len(data),len(data)) ]
    print("data ",data)
    print("npd ",npd)
    print("outer\n",outer)
    print("traces ",traces)
    # Should print
    """
    data  [3, 4, -2, 5]
    npd  [ 3  4 -2  5]
    outer
     [[ 15  20 -10  25]
     [ -6  -8   4 -10]
     [ 12  16  -8  20]
     [  9  12  -6  15]]
    traces  [9, 24, 4, 14, 44, -20, 25]
    """

