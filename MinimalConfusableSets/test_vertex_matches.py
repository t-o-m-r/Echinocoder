
import vertex_matches
from itertools import zip_longest

# Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.
# "Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).


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

def test():

    test_programme = [
        (None, 2, vertex_matches.generate_all_canonical_matches, M2_all_canonical_matches_expected, "M2 all",),
        (None, 3, vertex_matches.generate_all_canonical_matches, M3_all_canonical_matches_expected, "M3 all",),
        (None, 4, vertex_matches.generate_all_canonical_matches, M4_all_canonical_matches_expected, "M4 all",),
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

