# Encode list of n real (or complex) numbers treated as an element of a realprojectiveplane.  Encoding is length 2n-1 list of real (or complex) numbers.
# E.g. this method can encode ordered lists like this
#
#        x = [3,4,-2,5]
#
# which are deemed to be equivalent to their negations:
#
#        -x = [-3,-4,2,-5].
#
# Each of the above examples should encode to
#
#        [9, 24, 4, 14, 44, -20, 25]
#
# as in general [x1,x2,x3,..,xn] encodes to
#
#       [
#        x1*x1,
#        x1*x2 + x2*x1,
#        x1*x3 + x2*x2 + x3*x1,
#        ...
#        x1*xn + x2*x(n-1) + ... + xn*x1
#        ...
#        x(n-2)*xn + x(n-1)*x(n-1) + xn*x(n-2),
#        x(n-1)*xn + xn*x(n-1),
#        xn*xn,
#       ]
#
# which is of length 2n-1. 
#

import numpy as np

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

