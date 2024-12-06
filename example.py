#!/usr/bin/env python3

"""
Running this script should generate output resembling the following:

The set of vectors 
[[ 8 -1 -4  3]
 [-8 -5  9  7]
 [ 8  2  7 -7]]
embeds to 
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
Nonetheless, it embeds to 
[   8.   -4.  -57.  -80. -488. -394.    8.   12.  -63.  144. -952.  636.
    8.    3.  -15.  112. -456.  851.   -4.   12.   -6.  -21.    5.  309.
   -4.    3.   42.   40. -186.   68.   12.    3.   48.   34. -406.  392.]
too.


If we change one of the vectors by a small amount, the embedding changes by only a small amount. E.g.
[[ 8.    -1.    -4.     3.   ]
 [-8.    -5.     9.     7.   ]
 [ 8.     2.     7.    -7.001]]
embeds to:
[   8.      -4.     -57.     -80.    -488.    -394.       8.      12.
  -63.     144.    -952.     636.       8.       2.999  -14.99   112.
 -455.968  851.085   -4.      12.      -6.     -21.       5.     309.
   -4.       2.999   42.01    40.006 -186.022   68.016   12.       2.999
   48.01    33.995 -406.001  392.057]

Now let's try some other embedders

Using the simplex embedder ... 
... we find that the ouput is [ 4.71175355  5.97716044  2.27870903  6.31338771  4.50981973 10.55305146
  7.39127809  9.11676996  5.40387331  5.29204317 12.18165909  7.91533274
  6.34160765  6.40703423  6.30875449  8.19956912  3.62518034  7.35944864
  4.40777783 12.99478808 12.77917328 10.71712844  7.73758228  9.
 -8.        ].

Using the dotting embedder ... 
... we find that the ouput is [ -8.           8.           8.          -5.          -1.
   2.          -4.           7.           9.          -7.
   3.           7.          -1.10904362   4.49028978   6.15278722
  -7.02170733  -1.0637313   20.84294686 -12.81292792  -1.74738463
   6.63680093].

"""

import numpy as np


set_of_vectors_to_embed = np.array([
      (8,-1,-4,3),
      (-8,-5,9,7),
      (8,2,7,-7)])
another_set_of_vectors_to_embed = np.array([
      (8,2,7,-7),
      (8,-1,-4,3),
      (-8,-5,9,7)])
tweaked_set_of_vectors_to_embed = np.array([
      (8,-1,-4,3),
      (-8,-5,9,7),
      (8,2,7,-7.001)])

import Cinf_numpy_polynomial_embedder_for_array_of_reals_as_multiset as Cinf_np_ar
embedder = Cinf_np_ar.Embedder()

embedding = embedder.embed(set_of_vectors_to_embed)
another_embedding = embedder.embed(another_set_of_vectors_to_embed)

expected_embedding = [   8,   -4,  -57,  -80, -488, -394,    8,   12,  -63,  144, -952,  636, 8,    3,  -15,  112, -456,  851,   -4,   12,   -6,  -21,    5,  309, -4,    3,   42,   40, -186,   68,   12,    3,   48,   34, -406,  392]

print(f"The set of vectors \n{set_of_vectors_to_embed}\nembeds to \n{embedding}.\nWe expected\n{expected_embedding}\n\n")
print(f"Another set of vectors \n{another_set_of_vectors_to_embed}\ndiffers from the first by a permutation of the vectors.\nNonetheless, it embeds to \n{another_embedding}\ntoo.\n\n")
print(f"If we change one of the vectors by a small amount, the embedding changes by only a small amount. E.g.\n{tweaked_set_of_vectors_to_embed}\nembeds to:")
print(embedder.embed(tweaked_set_of_vectors_to_embed))

print("")
print("Now let's try some other embedders")
print("")

import C0HomDeg1_simplicialComplex_embedder_1_for_array_of_reals_as_multiset as simplex
import C0HomDeg1_conjectured_dotting_embedder_for_array_of_reals_as_multiset as conjectured_dotting

embedders_to_try = (
                     ("simplex", simplex.Embedder()),
                     ("dotting", conjectured_dotting.Embedder(n=3, k=4)), # This embedder needs to specialise on particular n and k
                   )

for name, embedder in embedders_to_try:
    print(f"Using the {name} embedder ... ")
    embedding = embedder.embed(set_of_vectors_to_embed)
    print(f"... we find that the ouput is {embedding}.")
    print()


   

