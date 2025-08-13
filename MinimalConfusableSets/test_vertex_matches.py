
from vertex_matches import (
    generate_all_vertex_matches,
    generate_all_vertex_match_signatures,
    _smallest_odd_number_greater_than_or_equal_to,
    generate_all_vertex_matches_given_equivalent_places,
    generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A,
    generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B,
)

from _vertex_matches import (
    generate_all_useful_vertex_matches,
    generate_all_vertex_matches_given_perming_places,
    generate_all_useful_vertex_matches_given_perming_places,
)

from equivalent_places import Equivalent_Places
from itertools import zip_longest

# Vertex matches have an even number of +1 and and odd number of -1 entries, and others zero. Their total number of entries is M, the numnber of bad bats.
# The "signature" of a vertex match is how many ones, minus ones and zeros it contains.
# "Useful" vertex matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).
# A "canonical" vertex match is one where all the ones come before all the minus ones which come before all the zeros WITHIN any positions which are otherwise equivalent. . E.g., of all position are equivalent, then (1,1,-1,-1,-1,0) is a canonical match.

M0_all_vertex_matches_expected = [
]

M1_all_vertex_matches_expected = [
    (-1,),
]

M2_all_vertex_matches_expected = [
    ( 0,-1),
    (-1, 0),
]

M3_all_vertex_matches_expected = [
    ( 0, 0,-1),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 1,-1),
    ( 1,-1, 1),
    (-1, 1, 1),
    (-1,-1,-1),
]
M3_all_vertex_match_signatures_expected = [
    ( 0,1,2), # for
              # ( 0, 0,-1),
              # ( 0,-1, 0),
              # (-1, 0, 0),
    (2,1,0), # for
              # ( 1, 1,-1),
              # ( 1,-1, 1),
              # (-1, 1, 1),
    (0,3,0), # for
              # (-1,-1,-1),
]

M4_all_vertex_matches_expected = [
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

M4_left_pair_right_pair = [
     #( 0, 0, 0,-1,),
     ( 0, 0,-1, 0,),#
     #( 0,-1, 0, 0,),
     (-1, 0, 0, 0,),#

     #( 0, 1, 1,-1,),
     ( 0, 1,-1 ,1,),#
     #( 0,-1, 1, 1,),
     #( 1, 0, 1,-1,),
     #( 1, 0,-1 ,1,),
     (-1, 0, 1, 1,),
     #( 1, 1, 0,-1,),
     #( 1,-1, 0, 1,),
     (-1, 1, 0, 1,),#
     ( 1, 1,-1, 0,),#
     #( 1,-1 ,1, 0,),
     #(-1, 1, 1, 0,),

     #( 0,-1,-1,-1,),
     (-1, 0,-1,-1,),#
     #(-1,-1, 0,-1,),
     (-1,-1,-1, 0,),#
    ]

k2M4_all_useful_vertex_match_signatures_expected = [
     #(0,1,3), # for
     #         # ( 0, 0, 0,-1,),
     #         # ( 0, 0,-1, 0,),
     #         # ( 0,-1, 0, 0,),
     #         # (-1, 0, 0, 0,),

     (2,1,1), # for
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
      (0,3,1), #for
              # ( 0,-1,-1,-1,),
              # (-1, 0,-1,-1,),
              # (-1,-1, 0,-1,),
              # (-1,-1,-1, 0,),
    ]
M4_all_vertex_match_signatures_expected = [
     (0,1,3), # for
              # ( 0, 0, 0,-1,),
              # ( 0, 0,-1, 0,),
              # ( 0,-1, 0, 0,),
              # (-1, 0, 0, 0,),

     (2,1,1), # for
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
      (0,3,1), #for
              # ( 0,-1,-1,-1,),
              # (-1, 0,-1,-1,),
              # (-1,-1, 0,-1,),
              # (-1,-1,-1, 0,),
    ]

k2M3_all_useful_vertex_matches_expected = [
    # ( 0, 0,-1),
    # ( 0,-1, 0),
    # (-1, 0, 0),
    ( 1, 1,-1),
    ( 1,-1, 1),
    (-1, 1, 1),
    (-1,-1,-1),
]
k2M4_all_useful_vertex_matches_expected = [
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
k2M4_all_useful_vertex_matches_with_1_perming_places = [
     #( 0, 0, 0,-1,),
     #( 0, 0,-1, 0,),
     #( 0,-1, 0, 0,),
     #(-1, 0, 0, 0,),

     #( 0, 1, 1,-1,),
     #( 0, 1,-1 ,1,),
     ( 0,-1, 1, 1,),
     #( 1, 0, 1,-1,),
     #( 1, 0,-1 ,1,),
     (-1, 0, 1, 1,),
     #( 1, 1, 0,-1,),
     ( 1,-1, 0, 1,),
     #(-1, 1, 0, 1,),
     #( 1, 1,-1, 0,),
     #( 1,-1 ,1, 0,),
     #(-1, 1, 1, 0,),

     ( 0,-1,-1,-1,),
     #(-1, 0,-1,-1,),
     #(-1,-1, 0,-1,),
     (-1,-1,-1, 0,),
]
k2M4_all_useful_vertex_matches_with_2_perming_places = [
     #( 0, 0, 0,-1,),
     #( 0, 0,-1, 0,),
     #( 0,-1, 0, 0,),
     #(-1, 0, 0, 0,),

     #( 0, 1, 1,-1,),
     ( 0, 1,-1 ,1,),
     ( 0,-1, 1, 1,),
     #( 1, 0, 1,-1,),
     ( 1, 0,-1 ,1,),
     (-1, 0, 1, 1,),
     #( 1, 1, 0,-1,),
     ( 1,-1, 0, 1,),
     (-1, 1, 0, 1,),
     ( 1, 1,-1, 0,),
     #( 1,-1 ,1, 0,),
     #(-1, 1, 1, 0,),

     ( 0,-1,-1,-1,),
     (-1, 0,-1,-1,),
     #(-1,-1, 0,-1,),
     (-1,-1,-1, 0,),
]
k3M4_all_useful_vertex_matches_expected = [
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

"""
All USEFUL matches in k=2 dimensions, given M=4 bad bats, for perming_places=1
   1:    (0, -1, -1, -1)
   2:    (-1, -1, -1, 0)
   3:    (0, 1, 1, -1)
   4:    (-1, 1, 1, 0)
   5:    (1, 1, -1, 0)

All USEFUL matches in k=2 dimensions, given M=4 bad bats, for perming_places=2
   1:    (-1, 0, -1, -1)
   2:    (0, -1, -1, -1)
   3:    (-1, -1, -1, 0)
   4:    (-1, 0, 1, 1)
   5:    (0, -1, 1, 1)
   6:    (0, 1, 1, -1)
   7:    (1, 0, 1, -1)
   8:    (-1, 1, 1, 0)
   9:    (1, -1, 1, 0)
   10:    (1, 1, -1, 0)

"""

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
        z = _smallest_odd_number_greater_than_or_equal_to(x)
        print(f"We hope that the smallest odd number greater than or equal to {x} is {y} and is also {z}")
        assert z==y
 
def test_signatures():
    test_programme = [
        (3, None, M3_all_vertex_match_signatures_expected, "M3 signatures"),
        (4, None, M4_all_vertex_match_signatures_expected, "M4 signatures"),
        (4, 2, k2M4_all_useful_vertex_match_signatures_expected, "k2M4 useful signatures"),
        ]
    for M, k, expected_signature, name in test_programme:
        LHS = sorted(list(generate_all_vertex_match_signatures(M=M, k=k)))
        RHS = sorted(expected_signature)

        print(f"Test '{name}' has LHS and RHS:")
        print("[")
        for i,j in zip_longest(LHS,RHS):
            print(f"({i}, {j}), ")
        print("]")

        print()

        assert LHS==RHS

def test_main_generators():

    test_programme = [
        (None, 0, generate_all_vertex_matches(M=0), M0_all_vertex_matches_expected, "M0 all",),
        (None, 1, generate_all_vertex_matches(M=1), M1_all_vertex_matches_expected, "M1 all",),
        (None, 2, generate_all_vertex_matches(M=2), M2_all_vertex_matches_expected, "M2 all",),
        (None, 3, generate_all_vertex_matches(M=3), M3_all_vertex_matches_expected, "M3 all",),
        (None, 4, generate_all_vertex_matches(M=4), M4_all_vertex_matches_expected, "M4 all",),
        (2, 3, generate_all_useful_vertex_matches(k=2, M=3), k2M3_all_useful_vertex_matches_expected, "k2M3 useful",),
        (2, 4, generate_all_useful_vertex_matches(k=2, M=4), k2M4_all_useful_vertex_matches_expected, "k2M4 useful",),
        (3, 4, generate_all_useful_vertex_matches(k=3, M=4), k3M4_all_useful_vertex_matches_expected, "k3M4 useful",),

        (2, 4, generate_all_useful_vertex_matches_given_perming_places(k=2, M=4,perming_places=4), k2M4_all_useful_vertex_matches_expected, "k2M4 useful but testing perming_places=4}",),
        (2, 4, generate_all_useful_vertex_matches_given_perming_places(k=2, M=4, perming_places=4), list(generate_all_useful_vertex_matches(M=4, k=2, permute=True)), "k2M4 useful but testing perming_places=4}",), # permute=True is like perming_places=M
        (2, 4, generate_all_useful_vertex_matches_given_perming_places(k=2, M=4, perming_places=3), list(generate_all_useful_vertex_matches(k=2, M=4, permute=True)), "k2M4 useful but testing perming_places=3}",), # permute=True is also like perming_places=M-1
        (2, 4, generate_all_useful_vertex_matches_given_perming_places(k=2, M=4, perming_places=2), k2M4_all_useful_vertex_matches_with_2_perming_places, "k2M4 useful but testing perming_places=2}",),
        (2, 4, generate_all_useful_vertex_matches_given_perming_places(k=2, M=4, perming_places=1), k2M4_all_useful_vertex_matches_with_1_perming_places, "k2M4 useful but testing perming_places=1}",),
        (2, 4, generate_all_useful_vertex_matches_given_perming_places(k=2, M=4, perming_places=0), list(generate_all_useful_vertex_matches(M=4, k=2, permute=False)), "k2M4 useful but testing perming_places=0}",),

        (None, 4, generate_all_vertex_matches_given_perming_places(M=4, perming_places=4), M4_all_vertex_matches_expected, "M4 but testing perming_places=4}",),
        (None, 4, generate_all_vertex_matches_given_perming_places(M=4, perming_places=4), list(generate_all_vertex_matches(M=4, permute=True)), "M4 but testing perming_places=4}",), # permute=True is like perming_places=M
        (None, 4, generate_all_vertex_matches_given_perming_places(M=4, perming_places=3), list(generate_all_vertex_matches(M=4, permute=True)), "M4 but testing perming_places=3}",), # permute=True is also like perming_places=M-1
        (None, 4, generate_all_vertex_matches_given_perming_places(M=4, perming_places=0), list(generate_all_vertex_matches(M=4, permute=False)), "M4 but testing perming_places=0}",),


        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(size=4, all_equivalent=True) ), list(generate_all_vertex_matches(M=4, permute=False)), "M4 but testing equivalent_places ALL",),
        # which should be the same as
        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,1,2,3,),    )) ), list(generate_all_vertex_matches_given_perming_places(M=4, perming_places=0)), "M4 but using equivalent_places to regenerate perming places 0",),
        # which leads to this sequence:
        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,),(1,2,3,),    )) ), list(generate_all_vertex_matches_given_perming_places(M=4, perming_places=1)), "M4 but using equivalent_places to regenerate perming places 1",),
        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,),(1,),(2,3,),    )) ), list(generate_all_vertex_matches_given_perming_places(M=4, perming_places=2)), "M4 but using equivalent_places to regenerate perming places 2",),
        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,),(1,),(2,),(3,),    )) ), list(generate_all_vertex_matches_given_perming_places(M=4, perming_places=3)), "M4 but equivalent_places to regenerate perming places 3",),
        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,),(1,),(2,),(3,),    )) ), list(generate_all_vertex_matches_given_perming_places(M=4, perming_places=4)), "M4 but equivalent_places to regenerate perming places 4",),
        # which should be the same as:
        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(size=4, none_equivalent=True) ), list(generate_all_vertex_matches(M=4, permute=True)), "M4 but testing equivalent_places NONE",),

        (None, 4, generate_all_vertex_matches_given_equivalent_places(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,1,),(2,3,),    )) ), M4_left_pair_right_pair, "M4 left pair right pair",),

        (None, 10,
     generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,7,),(1,4,5,6),(2,3,9,), (8,),  ))), 
     generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,7,),(1,4,5,6),(2,3,9,), (8,),  ))), 
      "Big 10 test.",),

        ]

    for k, M, gen, expected, name in test_programme:
 

        gen = tuple(gen)
        print(f"Test '{name}' has LHS and RHS:")
        print(f"gen {gen}")
        print(f"expected {expected}")

        LHS = sorted(gen)
        RHS = sorted(expected)

        print("[")
        for idx, (i,j) in enumerate(zip_longest(LHS,RHS)):
            print(f"{idx+1}:  ({i} {'==' if i==j else '!='} {j}), ")
        print("]")

        print()

        assert LHS==RHS

def test_order():
    
    for gen in (
          generate_all_vertex_matches(M=4),
          generate_all_vertex_matches(M=6),
          # WILL NOTE WORK: generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_A(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,7,),(1,4,5,6),(2,3,9,), (8,),  ))),
          # WILL NOTE WORK: generate_all_vertex_matches_given_equivalent_places_IMPLEMENTATION_B(equivalent_places = Equivalent_Places(equivalents_with_singletons=( (0,7,),(1,4,5,6),(2,3,9,), (8,),  ))),
          ):
        print(f"\n New Order Test")
        last_signature, last_vertex_match = None, None
        for vertex_match in gen:
            signature = vertex_match.count(-1), vertex_match.count(0), vertex_match.count(+1)
            print(f"order test saw signature={signature} and vm={vertex_match}")
            # Only check_order progression when within a given signature:
            if last_signature != None and signature == last_signature:
                # Check_order!
                assert last_vertex_match < vertex_match
            last_signature, last_vertex_match = signature, vertex_match



                


