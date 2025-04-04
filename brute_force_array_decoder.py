#!/usr/bin/env python 

"""
The purpose of this script is to provide a method that will attempt a brute force decoding of any array encoder which outputs "input_data" within its metadata.
"""

import numpy as np
import C0HomDeg1_simplicialComplex_embedder_2_for_array_of_reals_as_multiset as simplex2


embedder = simplex2.Embedder()

data = np.array([[1,2,3],
                 [4,-5,6],
                 [-7,8,9]])

encoding, (n,k), metadata = embedder.embed(data)

print(f"data = {data}")
print(f"ecoding = {encoding}")
print(f"metadata = {metadata}")
