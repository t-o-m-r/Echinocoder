#!/usr/bin/env python3

"""
This should give output resembling the following:

The set of vectors
[[ 8 -1 -4  3]
 [-8 -5  9  7]
 [ 8  2  7 -7]]
 encoded to
[   8.   -4.  -57.  -80. -488. -394.    8.   12.  -63.  144. -952.  636.
    8.    3.  -15.  112. -456.  851.   -4.   12.   -6.  -21.    5.  309.
   -4.    3.   42.   40. -186.   68.   12.    3.   48.   34. -406.  392.].
We expected
[8, -4, -57, -80, -488, -394, 8, 12, -63, 144, -952, 636, 8, 3, -15, 112, -456, 851, -4, 12, -6, -21, 5, 309, -4, 3, 42, 40, -186, 68, 12, 3, 48, 34, -406, 392]


Another set of vectors
[[ 8  2  7 -7]
 [ 8 -1 -4  3]
 [-8 -5  9  7]]
differs from the first by a permutation of the vectors.
Nonetheless, it encodes to
[   8.   -4.  -57.  -80. -488. -394.    8.   12.  -63.  144. -952.  636.
    8.    3.  -15.  112. -456.  851.   -4.   12.   -6.  -21.    5.  309.
   -4.    3.   42.   40. -186.   68.   12.    3.   48.   34. -406.  392.]
too.

"""

import numpy as np
import Cinf_numpy_polynomial_encoder_for_array_of_reals_as_multiset as encoder_Cinf_np_ar


set_of_vectors_to_encode = np.array([
      (8,-1,-4,3),
      (-8,-5,9,7),
      (8,2,7,-7)])
another_set_of_vectors_to_encode = np.array([
      (8,2,7,-7),
      (8,-1,-4,3),
      (-8,-5,9,7)])

encoding = encoder_Cinf_np_ar.encode(set_of_vectors_to_encode)
another_encoding = encoder_Cinf_np_ar.encode(another_set_of_vectors_to_encode)

expected_encoding = [   8,   -4,  -57,  -80, -488, -394,    8,   12,  -63,  144, -952,  636, 8,    3,  -15,  112, -456,  851,   -4,   12,   -6,  -21,    5,  309, -4,    3,   42,   40, -186,   68,   12,    3,   48,   34, -406,  392]

print(f"The set of vectors \n{set_of_vectors_to_encode}\n encoded to \n{encoding}.\nWe expected\n{expected_encoding}\n\n")
print(f"Another set of vectors \n{another_set_of_vectors_to_encode}\ndiffers from the first by a permutation of the vectors.\nNonetheless, it encodes to \n{another_encoding}\ntoo.")


   

