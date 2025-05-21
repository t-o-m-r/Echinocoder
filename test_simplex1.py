#!/usr/bin/env python

from C0HomDeg1_simplicialComplex_embedder_1_for_array_of_reals_as_multiset import *
from EncDec import simplex_1_embed

def test_simplex1():
    data_1 = np.asarray([[8,-1,-4,3],[-8,-5,9,7],[8,2,7,-7]])

    embedder = Embedder()
    output_1 = embedder.embed(data_1, debug=False)

    output_2 = simplex_1_embed(data_1, injection_method="legacy")

    print(f"Output 1\n{output_1}")

    expected_1 = (
        np.array([ 4.71175355174112, 5.977160438028798, 2.2787090323608865, 6.313387708574837, 4.509819730223158, 10.553051460643722, 7.391278090867309, 9.116769964309757, 5.403873305930562, 5.292043169210447, 12.181659089431442, 7.915332741728193, 6.341607654259072, 6.407034232226631, 6.308754488187963, 8.19956911811357, 3.6251803395690914, 7.359448640965423, 4.407777826681421, 12.994788083863279, 12.779173276088777, 10.717128436369887, 7.73758228104532, -8.0, ]),
         (3, 4), None)

    expected_2 = expected_1[0]
    

    for output, expected in (
          (output_1, expected_1),
          (output_2, expected_2),
          ):

        sout=str(output)
        sexp=str(expected)

        print(f"sout={sout}\nsexp={sexp}\n")
        assert sout == sexp



if __name__ == "__main__":
    test_simplex2()
