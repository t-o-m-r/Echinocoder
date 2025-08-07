#!/usr/bin/env python3

import numpy as np
import time

debug = False

set_of_vectors_to_embed = np.random.rand(20,4)
loops = 10

n,k = set_of_vectors_to_embed.shape

test_sets_of_vectors = [ 
        set_of_vectors_to_embed,
    ]

import C0HomDeg1_simplicialComplex_embedder_1_for_array_of_reals_as_multiset as simplex1
import C0HomDeg1_simplicialComplex_embedder_2_for_array_of_reals_as_multiset as simplex2
import C0HomDeg1_conjectured_dotting_embedder_for_array_of_reals_as_multiset as conjectured_dotting

some_embedders = [ 
    simplex1.Embedder(simplex1.Embedder.Method.LEGACY),
    simplex1.Embedder(simplex1.Embedder.Method.ENCDEC1LEGACY),
    simplex2.Embedder(),
    conjectured_dotting.Embedder(n, k),
]

for embedder in some_embedders:

  for arr in test_sets_of_vectors:
    
    #print(f"\n==========================\nVectors to be encoded are:|")
    #for vec in arr:
    #   print(f"{vec}, ") 
   
    t0 = time.time()
    for loop in range(loops):
       embedding, (n_out, k_out), metadata = embedder.embed(arr, debug=False)
    t1 = time.time()
    print(t1-t0," sec for ",loops," loops at (n,k)=",arr.shape, " with ", embedder)

