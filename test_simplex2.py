#!/usr/bin/env python

from C0HomDeg1_simplicialComplex_embedder_2_for_array_of_reals_as_multiset import *

def test_simplex2():
    data_1 = np.asarray([[4,2,3],
                         [-3,5,1],
                         [8,9,2],
                         [2,7,2]])

    data_2 = np.asarray([[4,3,3],
                         [-3,5,1],
                         [8,9,2],
                         [2,6,2]])
    embedder = Embedder()
    output_1 = embedder.embed(data_1, debug=False)
    output_2 = embedder.embed(data_2, debug=False)

    print(f"Output 1\n{output_1}")
    print(f"Output 2\n{output_2}")

    expected_1 = ( np.array([-3.        ,  2.        ,  1.        , 13.65999692,  8.21161772,
       12.9785852 , 11.88854796, 14.44465641, 11.99260699, 11.77453054,
       11.86600792, 13.28731004,  8.99661582, 12.10852268,  4.95057157,
        9.90426914,  9.26064312, 12.02676068,  9.56793264, 11.73087378,
        9.01771478, 13.63840125]), (4, 3), {'ascending_data': np.array([[-3,  2,  1],
       [ 2,  5,  2],
       [ 4,  7,  2],
       [ 8,  9,  3]]), 'input_data': np.array([[ 4,  2,  3],
       [-3,  5,  1],
       [ 8,  9,  2],
       [ 2,  7,  2]])})

    expected_2 = (np.array([-3.        ,  3.        ,  1.        , 10.75554923, 10.76276404,
       11.01418014,  7.19559146, 11.3924411 ,  7.4648976 ,  8.33175766,
       11.53835055, 11.24548369,  7.48823886, 11.15220393,  3.74046917,
        6.44599078,  4.73942503, 11.18122614,  8.75195152,  8.42249382,
        8.50812563, 10.31175688]), (4, 3), {'ascending_data': np.array([[-3,  3,  1],
       [ 2,  5,  2],
       [ 4,  6,  2],
       [ 8,  9,  3]]), 'input_data': np.array([[ 4,  3,  3],
       [-3,  5,  1],
       [ 8,  9,  2],
       [ 2,  6,  2]])})

    

    for output, expected in ((output_1, expected_1),(output_2, expected_2)):

        sout=str(output)
        sexp=str(expected)

        print(f"sout={sout}\nsexp={sexp}\n")
        assert sout == sexp



if __name__ == "__main__":
    test_simplex2()
