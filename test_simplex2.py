#!/usr/bin/env python

from C0HomDeg1_simplicialComplex_embedder_2_for_array_of_reals_as_multiset import *

if __name__ == "__main__":

    data_1 = np.asarray([[4,2,3],
                         [-3,5,1],
                         [8,9,2],
                         [2,7,2]])

    data_2 = np.asarray([[4,3,3],
                         [-3,5,1],
                         [8,9,2],
                         [2,6,2]])
    embedder = Embedder()
    output_1 = embedder.embed(data_1, debug=True)
    output_2 = embedder.embed(data_2, debug=False)

    print(f"Output 1\n{output_1}")
    print(f"Output 2\n{output_2}")
    
