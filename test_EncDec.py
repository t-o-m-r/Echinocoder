from fractions import Fraction
from itertools import pairwise
import numpy as np

from EncDec import ArrayToLinComb
from EncDec import BarycentricSubdivide
from EncDec import Chain
from EncDec import pretty_print_lin_comb
from tools import numpy_array_of_frac_to_str

#def test_BarycentricSubdivide_split_not_preserving_scale():
#    print("###########################################")
#
#    subdivide = BarycentricSubdivide("pIn","pOut", "qOut", preserve_scale=False)
#
#    input_dict = {"pIn": [(-1, np.array([1, 0, 0])),
#                        (-7, np.array([0, 1, 0])),
#                        (10, np.array([0, 0, 1]))],
#                  "metadata1": "moo1",
#                  "metadata2": "moo2",
#                  "metadata3": "moo3",
#                  }
#    enc = subdivide.encode(input_dict, debug=True)
#    print(f"enc\n{enc}")
#    expected = "{'pOut': [(11, array([0, 0, 1])), (6, array([1, 0, 1]))], 'qOut': [(-7, array([1, 1, 1]))]}"
#    assert str(enc) == expected
#
#def test_BarycentricSubdivide_no_split_not_preserving_scale():
#    print("###########################################")
#
#    subdivide = BarycentricSubdivide("pIn","pOut", "pOut", preserve_scale=False)
#
#    input_dict = {"pIn": [(-1, np.array([1, 0, 0])),
#                        (-7, np.array([0, 1, 0])),
#                        (10, np.array([0, 0, 1]))],
#                  "metadata1": "moo1",
#                  "metadata2": "moo2",
#                  "metadata3": "moo3",
#                  }
#    enc = subdivide.encode(input_dict, debug=True)
#    print(f"enc\n{enc}")
#    expected = "{'pOut': [(11, array([0, 0, 1])), (6, array([1, 0, 1])), (-7, array([1, 1, 1]))]}"
#    assert str(enc) == expected
#
#def test_BarycentricSubdivide_no_split_preserve_scale():
#    print("###########################################")
#
#    subdivide = BarycentricSubdivide("pIn","pOut", "pOut")
#
#    input_dict = {"pIn": [(-1, np.array([1, 0, 0])),
#                        (-7, np.array([0, 1, 0])),
#                        (10, np.array([0, 0, 1]))],
#                  "metadata1": "moo1",
#                  "metadata2": "moo2",
#                  "metadata3": "moo3",
#                  }
#    enc = subdivide.encode(input_dict, debug=True)
#    print(f"enc\n{enc}")
#    expected = "{'pOut': [(11, array([Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)], dtype=object)), (12, array([Fraction(1, 2), Fraction(0, 1), Fraction(1, 2)], dtype=object)), (-21, array([Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)], dtype=object))]}"
#    assert str(enc) == expected
#
#
#def test_BarycentricSubdivide_split_preserve_scale():
#    print("###########################################")
#
#    subdivide = BarycentricSubdivide("pIn","pOut", "qOut")
#
#    input_dict = {"pIn": [(-1, np.array([1, 0, 0])),
#                        (-7, np.array([0, 1, 0])),
#                        (10, np.array([0, 0, 1]))],
#                  "metadata1": "moo1",
#                  "metadata2": "moo2",
#                  "metadata3": "moo3",
#                  }
#    enc = subdivide.encode(input_dict, debug=True)
#    print(f"enc\n{enc}")
#    expected = "{'pOut': [(11, array([Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)], dtype=object)), (12, array([Fraction(1, 2), Fraction(0, 1), Fraction(1, 2)], dtype=object))], 'qOut': [(-21, array([Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)], dtype=object))]}"
#    assert str(enc) == expected


def test_ArrayToLinComb():
    print("###########################################")

    arr = np.asarray([[ 4, 2],
                      [-3, 5],
                      [ 8, 9],
                      [ 2 ,7]])

    enc = ArrayToLinComb(arr)

    expected = """[(np.int64(4), array([[1, 0],
       [0, 0],
       [0, 0],
       [0, 0]])), (np.int64(2), array([[0, 1],
       [0, 0],
       [0, 0],
       [0, 0]])), (np.int64(-3), array([[0, 0],
       [1, 0],
       [0, 0],
       [0, 0]])), (np.int64(5), array([[0, 0],
       [0, 1],
       [0, 0],
       [0, 0]])), (np.int64(8), array([[0, 0],
       [0, 0],
       [1, 0],
       [0, 0]])), (np.int64(9), array([[0, 0],
       [0, 0],
       [0, 1],
       [0, 0]])), (np.int64(2), array([[0, 0],
       [0, 0],
       [0, 0],
       [1, 0]])), (np.int64(7), array([[0, 0],
       [0, 0],
       [0, 0],
       [0, 1]]))]"""

    print(f"=======================\nArray to lin comb made encoded")
    print(arr)
    print("to")
    print(f"{enc}")
    assert str(enc) == expected


#def test_Chain_1():
#    print("###########################################")
#    simplex1_bit = Chain([
#        BarycentricSubdivide("set", "first_diffs", "offset"),
#        BarycentricSubdivide("first_diffs", "second_diffs", "second_diffs", pass_forward="offset")
#    ])
#
#    input_dict = {
#                  "set": [(-1, np.array([1, 0, 0])),
#                          (-7, np.array([0, 1, 0])),
#                          (10, np.array([0, 0, 1]))],
#                  "metadata1": "moo1",
#                  "metadata2": "moo2",
#                  "metadata3": "moo3",
#                  }
#    enc = simplex1_bit.encode(input_dict, debug=True)
#    print(f"=======================\nSimplex1 as a chain encoded")
#    print(input_dict)
#    print("to")
#    print(f"{enc}")
#
#
#def test_simplex_1_initial_encoding_phase():
#    print("###########################################")
#    simplex1_different_bit = Chain([
#        ArrayToLinComb(input_array_name="set", output_lin_comb_name="lin_comb_0"),
#        BarycentricSubdivide("lin_comb_0", "lin_comb_1_first_diffs", "offset", preserve_scale=False),
#        BarycentricSubdivide("lin_comb_1_first_diffs", "lin_comb_2_second_diffs",
#                             "lin_comb_2_second_diffs", pass_forward="offset", pass_backward="offset", preserve_scale=False),
#        MergeLinCombs(["lin_comb_2_second_diffs", "offset"], "lin_comb_3"),
#    ])
#
#    input_dict = {
#                  "set" : np.asarray([[ 4, 2],
#                                      [-3, 5],
#                                      [ 8, 9],
#                                      [ 2 ,7]]),
#                  "metadata1": "moo1",
#                  "metadata2": "moo2",
#                  "metadata3": "moo3",
#                  }
#    enc = simplex1_different_bit.encode(input_dict, debug=True)
#    print(f"=======================\nSimplex1 as a chain encoded")
#    print(numpy_array_of_frac_to_str(input_dict["set"]))
#    print("to")
#    #print(f"{enc}")
#
#    lin_comb_3 = enc["lin_comb_3"]
#    #print(f"Note that lin_comb_3 is")
#    pretty_print_lin_comb(lin_comb_3)
#    print("and the (non-offset) differences are")
#    [ print(numpy_array_of_frac_to_str(tmp:=b-a), " with ", np.sum(tmp)," ones in it") for a,b in list(pairwise( [a for _,a in lin_comb_3 ]))[:-1] ]
#
#
#    print("###########################################")


