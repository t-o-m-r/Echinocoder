
import vertex_matches
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

     ( 0, 1, 1,-1,),
     #( 0, 1,-1 ,1,),
     #( 0,-1, 1, 1,),
     #( 1, 0, 1,-1,),
     #( 1, 0,-1 ,1,),
     #(-1, 0, 1, 1,),
     #( 1, 1, 0,-1,),
     #( 1,-1, 0, 1,),
     #(-1, 1, 0, 1,),
     ( 1, 1,-1, 0,),
     #( 1,-1 ,1, 0,),
     (-1, 1, 1, 0,),

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

     ( 0, 1, 1,-1,),
     #( 0, 1,-1 ,1,),
     ( 0,-1, 1, 1,),
     ( 1, 0, 1,-1,),
     #( 1, 0,-1 ,1,),
     (-1, 0, 1, 1,),
     #( 1, 1, 0,-1,),
     #( 1,-1, 0, 1,),
     #(-1, 1, 0, 1,),
     ( 1, 1,-1, 0,),
     ( 1,-1 ,1, 0,),
     (-1, 1, 1, 0,),

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

def tost_helper_functions():

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
 
    from vertex_matches import bi_range, bi_range_with_maxes, bi_range_with_maxes_crude

    assert list(bi_range(4)) == [ (0,4), (1,3), (2,2), (3,1), (4,0), ]
    assert list(bi_range(3)) == [ (0,3), (1,2), (2,1), (3,0), ]
    assert list(bi_range(2)) == [ (0,2), (1,1), (2,0), ]
    assert list(bi_range(1)) == [ (0,1), (1,0), ]
    assert list(bi_range(0)) == [ (0,0), ]
    assert list(bi_range(-1)) == [ ]
    assert list(bi_range(-2)) == [ ]
    assert list(bi_range(-3)) == [ ]

    for brwm in (bi_range_with_maxes_crude, bi_range_with_maxes):
        print("Using ",brwm)
        assert list(brwm(-3, 0, 0)) == [ ]
        assert list(brwm(-2, 0, 0)) == [ ]
        assert list(brwm(-1, 0, 0)) == [ ]
        assert list(brwm(0, 0, 0)) == [ (0,0), ]
        assert list(brwm(0, 1, 0)) == [ (0,0), ]
        assert list(brwm(0, 0, 3)) == [ (0,0), ]
        assert list(brwm(0, 1, 3)) == [ (0,0), ]
        assert list(brwm(4, 0, 0)) == [ ]
        assert list(brwm(4, 1, 1)) == [ ]
        assert list(brwm(4, -1, 4)) == [ ]
        assert list(brwm(4, 4, -1)) == [ ]
        assert list(brwm(4, -2, 4)) == [ ]
        assert list(brwm(4, 4, -2)) == [ ]
        assert list(brwm(4, 5, 1)) == [ (3,1), (4,0), ]
        assert list(brwm(4, 2, 4)) == [ (0,4), (1,3), (2,2), ]
        assert list(brwm(4, 1, 4)) == [ (0,4), (1,3), ]
        assert list(brwm(4, 2, 3)) == [ (1,3), (2,2), ]
        assert list(brwm(10, 2, 4)) == [ ]
        assert list(brwm(10, 2, 5)) == [ ]
        assert list(brwm(10, 2, 6)) == [ ]
        assert list(brwm(10, 2, 7)) == [ ]
        assert list(brwm(10, 2, 8)) == [ (2,8) ]
        assert list(brwm(10, 2, 9)) == [ (1,9), (2,8), ]
        assert list(brwm(10, 2, 10)) == [ (0,10), (1,9), (2,8), ]
        assert list(brwm(10, 2, 11)) == [ (0,10), (1,9), (2,8), ]
        assert list(brwm(10, 11, 2)) == [ (8,2), (9,1), (10,0), ]
        assert list(brwm(10, 10, 2)) == [ (8,2), (9,1), (10,0), ]
        assert list(brwm(10, 9, 2)) == [ (8,2), (9,1), ]
        assert list(brwm(10, 8, 2)) == [ (8,2), ]
        assert list(brwm(10, 7, 2)) == [ ]
        assert list(brwm(10, 6, 2)) == [ ]
        assert list(brwm(10, 5, 2)) == [ ]
        assert list(brwm(10, 4, 2)) == [ ]

def tost_signatures():
    test_programme = [
        (3, None, M3_all_vertex_match_signatures_expected, "M3 signatures"),
        (4, None, M4_all_vertex_match_signatures_expected, "M4 signatures"),
        (4, 2, k2M4_all_useful_vertex_match_signatures_expected, "k2M4 useful signatures"),
        ]
    for M, k, expected_signature, name in test_programme:
        LHS = sorted(list(vertex_matches.generate_all_vertex_match_signatures(M=M, k=k)))
        RHS = sorted(expected_signature)

        print(f"Test '{name}' has LHS and RHS:")
        print("[")
        for i,j in zip_longest(LHS,RHS):
            print(f"({i}, {j}), ")
        print("]")

        print()

        assert LHS==RHS

def test_main_generators():


    def set_perming_places(f, perming_places=0):
        return lambda k, M: f(M=M, k=k, perming_places=perming_places)
        
    test_programme = [
###        (None, 0, vertex_matches.generate_all_vertex_matches, M0_all_vertex_matches_expected, "M0 all",),
###        (None, 1, vertex_matches.generate_all_vertex_matches, M1_all_vertex_matches_expected, "M1 all",),
###        (None, 2, vertex_matches.generate_all_vertex_matches, M2_all_vertex_matches_expected, "M2 all",),
###        (None, 3, vertex_matches.generate_all_vertex_matches, M3_all_vertex_matches_expected, "M3 all",),
###        (None, 4, vertex_matches.generate_all_vertex_matches, M4_all_vertex_matches_expected, "M4 all",),
###        (2, 3, vertex_matches.generate_all_useful_vertex_matches, k2M3_all_useful_vertex_matches_expected, "k2M3 useful",),
###        (2, 4, vertex_matches.generate_all_useful_vertex_matches, k2M4_all_useful_vertex_matches_expected, "k2M4 useful",),
###        (3, 4, vertex_matches.generate_all_useful_vertex_matches, k3M4_all_useful_vertex_matches_expected, "k3M4 useful",),
###
###        (2, 4, set_perming_places(vertex_matches.generate_all_useful_matches_given_perming_places, perming_places=4), k2M4_all_useful_vertex_matches_expected, "k2M4 useful but testing perming_places=4}",),
###        (2, 4, set_perming_places(vertex_matches.generate_all_useful_matches_given_perming_places, perming_places=4), list(vertex_matches.generate_all_useful_vertex_matches(M=4, k=2, permute=True)), "k2M4 useful but testing perming_places=4}",), # permute=True is like perming_places=M
###        (2, 4, set_perming_places(vertex_matches.generate_all_useful_matches_given_perming_places, perming_places=3), list(vertex_matches.generate_all_useful_vertex_matches(k=2, M=4, permute=True)), "k2M4 useful but testing perming_places=3}",), # permute=True is also like perming_places=M-1
###        (2, 4, set_perming_places(vertex_matches.generate_all_useful_matches_given_perming_places, perming_places=2), k2M4_all_useful_vertex_matches_with_2_perming_places, "k2M4 useful but testing perming_places=2}",),
###        (2, 4, set_perming_places(vertex_matches.generate_all_useful_matches_given_perming_places, perming_places=1), k2M4_all_useful_vertex_matches_with_1_perming_places, "k2M4 useful but testing perming_places=1}",),
        (2, 4, set_perming_places(vertex_matches.generate_all_useful_matches_given_perming_places, perming_places=0), list(vertex_matches.generate_all_useful_vertex_matches(M=4, k=2, permute=False)), "k2M4 useful but testing perming_places=0}",),

###        (None, 4, set_perming_places(vertex_matches.generate_all_matches_given_perming_places, perming_places=4), M4_all_vertex_matches_expected, "M4 but testing perming_places=4}",),
###        (None, 4, set_perming_places(vertex_matches.generate_all_matches_given_perming_places, perming_places=4), list(vertex_matches.generate_all_vertex_matches(M=4, permute=True)), "M4 but testing perming_places=4}",), # permute=True is like perming_places=M
###        (None, 4, set_perming_places(vertex_matches.generate_all_matches_given_perming_places, perming_places=3), list(vertex_matches.generate_all_vertex_matches(M=4, permute=True)), "M4 but testing perming_places=3}",), # permute=True is also like perming_places=M-1
###        (None, 4, set_perming_places(vertex_matches.generate_all_matches_given_perming_places, perming_places=0), list(vertex_matches.generate_all_vertex_matches(M=4, permute=False)), "M4 but testing perming_places=0}",),
###
        ]

    for k, M, gen, expected, name in test_programme:
  
        LHS = sorted(gen(M=M, k=k))
        RHS = sorted(expected)

        print(f"Test '{name}' has LHS and RHS:")
        print("[")
        for i,j in zip_longest(LHS,RHS):
            print(f"({i}, {j}), ")
        print("]")

        print()

        assert LHS==RHS

