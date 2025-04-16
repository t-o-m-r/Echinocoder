from fractions import Fraction
from itertools import pairwise
import numpy as np

from EncDec import ArrayToLinComb
from EncDec import BarycentricSubdivide
from EncDec import Chain
from EncDec import PassThrough
from EncDec import MergeLinCombs
from EncDec import pretty_print_lin_comb
from tools import numpy_array_of_frac_to_str

def test_PassThrough():
    print("###########################################")

    pass_through = PassThrough()

    input = {"hello": "world"}
    enc = pass_through.encode(input)
    dec = pass_through.decode(enc)
    assert dec == input
    assert enc == input

def test_BarycentricSubdivide_no_split():
    print("###########################################")

    subdivide = BarycentricSubdivide("p","p", "q")

    input_dict = {"p": [(-1, np.array([1, 0, 0])),
                        (-7, np.array([0, 1, 0])),
                        (10, np.array([0, 0, 1]))],
                  "metadata1": "moo1",
                  "metadata2": "moo2",
                  "metadata3": "moo3",
                  }
    enc = subdivide.encode(input_dict, debug=True)
    print("no_split enc was")
    print(enc)
    expected = "{'p': [(11, array([Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)], dtype=object)), (12, array([Fraction(1, 2), Fraction(0, 1), Fraction(1, 2)], dtype=object))], 'q': [(-21, array([Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)], dtype=object))]}"
    assert str(enc) == expected


def test_BarycentricSubdivide_split():
    print("###########################################")

    subdivide = BarycentricSubdivide("p","p2", "q")

    input_dict = {"p": [(-1, np.array([1, 0, 0])),
                        (-7, np.array([0, 1, 0])),
                        (10, np.array([0, 0, 1]))],
                  "metadata1": "moo1",
                  "metadata2": "moo2",
                  "metadata3": "moo3",
                  }
    enc = subdivide.encode(input_dict, debug=True)
    print("split enc was")
    print(enc)
    expected = "{'p2': [(11, array([Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)], dtype=object)), (12, array([Fraction(1, 2), Fraction(0, 1), Fraction(1, 2)], dtype=object))], 'q': [(-21, array([Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)], dtype=object))]}"
    assert str(enc) == expected


def test_ArrayToLinComb():
    print("###########################################")

    input_dict = { "arr" : np.asarray([[ 4, 2],
                                       [-3, 5],
                                       [ 8, 9],
                                       [ 2 ,7]]) }
    array_to_lin_comb = ArrayToLinComb("arr", "lin_comb" )

    enc = array_to_lin_comb.encode(input_dict)
    print(f"=======================\nArray to lin comb made encoded")
    print(input_dict)
    print("to")
    print(f"{enc}")

    print("###########################################")
    simplex1_bit = Chain([
        BarycentricSubdivide("set", "first_diffs", "offset"),
        BarycentricSubdivide("first_diffs", "second_diffs", "second_diffs", pass_forward="offset")
    ])

    input_dict = {
                  "set": [(-1, np.array([1, 0, 0])),
                          (-7, np.array([0, 1, 0])),
                          (10, np.array([0, 0, 1]))],
                  "metadata1": "moo1",
                  "metadata2": "moo2",
                  "metadata3": "moo3",
                  }
    enc = simplex1_bit.encode(input_dict, debug=True)
    print(f"=======================\nSimplex1 as a chain encoded")
    print(input_dict)
    print("to")
    print(f"{enc}")



    print("###########################################")
    simplex1_different_bit = Chain([
        ArrayToLinComb(input_array_name="set", output_lin_comb_name="lin_comb_0"),
        BarycentricSubdivide("lin_comb_0", "lin_comb_1_first_diffs", "offset", preserve_scale=False),
        BarycentricSubdivide("lin_comb_1_first_diffs", "lin_comb_2_second_diffs",
                             "lin_comb_2_second_diffs", pass_forward="offset", pass_backward="offset", preserve_scale=False),
        MergeLinCombs(["lin_comb_2_second_diffs", "offset"], "lin_comb_3"),
    ])

    input_dict = {
                  "set" : np.asarray([[ 4, 2],
                                      [-3, 5],
                                      [ 8, 9],
                                      [ 2 ,7]]),
                  "metadata1": "moo1",
                  "metadata2": "moo2",
                  "metadata3": "moo3",
                  }
    enc = simplex1_different_bit.encode(input_dict, debug=True)
    print(f"=======================\nSimplex1 as a chain encoded")
    print(numpy_array_of_frac_to_str(input_dict["set"]))
    print("to")
    #print(f"{enc}")

    lin_comb_3 = enc["lin_comb_3"]
    #print(f"Note that lin_comb_3 is")
    pretty_print_lin_comb(lin_comb_3)
    print("and the (non-offset) differences are")
    [ print(numpy_array_of_frac_to_str(tmp:=b-a), " with ", np.sum(tmp)," ones in it") for a,b in list(pairwise( [a for _,a in lin_comb_3 ]))[:-1] ]


    print("###########################################")


