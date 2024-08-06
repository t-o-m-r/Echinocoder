# Encode list of real numbers treated as multiset.
# E.g. this method can encode things like:
#
#        [3,4,-2,]
#
# representing the multiset
#
#       {{ 3, 4, -2 }}
#
# Although this implementation claims to only do reals, it does in fact (privately) encode complex lists, albeit to complex outputs.


name="Cinf_numpy_polynomial_encoder_for_list_of_reals_as_multiset"

import numpy as np

def encode(data):
    return np.polynomial.polynomial.polyfromroots(-data)[-2::-1] # The -1 in [-2::-1] reverses the order of the list so that the terms linear in the roots come first. The -2 at the front forced the list to start from the coeffient for x^(n-1). (The coefficient of x^n is always 1 and we dont need it!)


    ## Alternative:
    #
    # import tools
    # ans = np.polynomial.polynomial.polyfromroots(-data)[-2::-1] # The -1 in [-2::-1] reverses the order of the list so that the terms linear in the roots come first. The -2 at the front forced the list to start from the coeffient for x^(n-1). (The coefficient of x^n is always 1 and we dont need it!)

    ## All encoders have to output lists of real numbers (at least for now) so:
    #if np.iscomplexobj(ans):
    #  ans=tools.expand_complex_to_real_pairs(ans)
    #
    #return ans
