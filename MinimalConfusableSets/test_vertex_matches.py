
import vertex_matches
from itertools import zip_longest

# Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.
# "Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).


M0_all_canonical_matches_expected = [
]

M1_all_canonical_matches_expected = [
    (-1,),
]

M2_all_canonical_matches_expected = [
    ( 0,-1),
    (-1, 0),
]

M3_all_canonical_matches_expected = [
    ( 0, 0,-1),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 1,-1),
    ( 1,-1, 1),
    (-1, 1, 1),
    (-1,-1,-1),
]

M4_all_canonical_matches_expected = [
     ( 0, 0, 0,-1,),
     ( 0, 0,-1, 0,),
     ( 0,-1, 0, 0,),
     (-1, 0, 0, 0,),

     ( 0, 1, 1,-1,),
     ( 0, 1,-1 ,1,),
     ( 0,-1, 1, 1,),
     ( 1, 0, 1,-1,),
     ( 1, 0,-1 ,1,),
     (-1, 0, 1, 1,),
     ( 1, 1, 0,-1,),
     ( 1,-1, 0, 1,),
     (-1, 1, 0, 1,),
     ( 1, 1,-1, 0,),
     ( 1,-1 ,1, 0,),
     (-1, 1, 1, 0,),

     ( 0,-1,-1,-1,),
     (-1, 0,-1,-1,),
     (-1,-1, 0,-1,),
     (-1,-1,-1, 0,),

    ]

k2M3_all_useful_canonical_matches_expected = [
    # ( 0, 0,-1),
    # ( 0,-1, 0),
    # (-1, 0, 0),
    ( 1, 1,-1),
    ( 1,-1, 1),
    (-1, 1, 1),
    (-1,-1,-1),
]
k2M4_all_useful_canonical_matches_expected = [
     #( 0, 0, 0,-1,),
     #( 0, 0,-1, 0,),
     #( 0,-1, 0, 0,),
     #(-1, 0, 0, 0,),

     ( 0, 1, 1,-1,),
     ( 0, 1,-1 ,1,),
     ( 0,-1, 1, 1,),
     ( 1, 0, 1,-1,),
     ( 1, 0,-1 ,1,),
     (-1, 0, 1, 1,),
     ( 1, 1, 0,-1,),
     ( 1,-1, 0, 1,),
     (-1, 1, 0, 1,),
     ( 1, 1,-1, 0,),
     ( 1,-1 ,1, 0,),
     (-1, 1, 1, 0,),

     ( 0,-1,-1,-1,),
     (-1, 0,-1,-1,),
     (-1,-1, 0,-1,),
     (-1,-1,-1, 0,),

    ]
k3M4_all_useful_canonical_matches_expected = [
     # ( 0, 0, 0,-1,),
     # ( 0, 0,-1, 0,),
     # ( 0,-1, 0, 0,),
     # (-1, 0, 0, 0,),

     # ( 0, 1, 1,-1,),
     # ( 0, 1,-1 ,1,),
     # ( 0,-1, 1, 1,),
     # ( 1, 0, 1,-1,),
     # ( 1, 0,-1 ,1,),
     # (-1, 0, 1, 1,),
     # ( 1, 1, 0,-1,),
     # ( 1,-1, 0, 1,),
     # (-1, 1, 0, 1,),
     # ( 1, 1,-1, 0,),
     # ( 1,-1 ,1, 0,),
     # (-1, 1, 1, 0,),

     # ( 0,-1,-1,-1,),
     # (-1, 0,-1,-1,),
     # (-1,-1, 0,-1,),
     # (-1,-1,-1, 0,),

    ]

def test_helper_functions():

    for x,y in [
            (-0.5, 1),
            (0, 1),
            (1, 1),
            (1.1, 3),
            (2, 3),
            (3, 3),
            (3.0001, 5),
            (3.2, 5),
            (4.2, 5),
            (4.9999, 5),
            (5, 5),
            (5.0001, 7),
            ]:
        z = vertex_matches.smallest_odd_number_greater_than_or_equal_to(x)
        print(f"We hope that the smallest odd number greater than or equal to {x} is {y} and is also {z}")
        assert z==y

def test_main_generators():

    test_programme = [
        (None, 0, vertex_matches.generate_all_canonical_matches, M0_all_canonical_matches_expected, "M0 all",),
        (None, 1, vertex_matches.generate_all_canonical_matches, M1_all_canonical_matches_expected, "M1 all",),
        (None, 2, vertex_matches.generate_all_canonical_matches, M2_all_canonical_matches_expected, "M2 all",),
        (None, 3, vertex_matches.generate_all_canonical_matches, M3_all_canonical_matches_expected, "M3 all",),
        (None, 4, vertex_matches.generate_all_canonical_matches, M4_all_canonical_matches_expected, "M4 all",),
        (2, 3, vertex_matches.generate_all_useful_canonical_matches, k2M3_all_useful_canonical_matches_expected, "k2M3 useful",),
        (2, 4, vertex_matches.generate_all_useful_canonical_matches, k2M4_all_useful_canonical_matches_expected, "k2M4 useful",),
        (3, 4, vertex_matches.generate_all_useful_canonical_matches, k3M4_all_useful_canonical_matches_expected, "k3M4 useful",),
        ]

    for k, M, gen, expected, name in test_programme:
  
        LHS = sorted(gen(k=k, M=M))
        RHS = sorted(expected)

        print(f"Test '{name}' has LHS and RHS:")
        print("[")
        for i,j in zip_longest(LHS,RHS):
            print(f"({i}, {j}), ")
        print("]")

        print()

        assert LHS==RHS

