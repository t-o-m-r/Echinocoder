
import vertex_matches

# Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.
# "Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).



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

k4M4_all_useful_canonical_matches_expected = [
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

def test():

    test_programme = [
        (2, 4, vertex_matches.generate_all_canonical_matches, M4_all_canonical_matches_expected, "M4 all",)
        ]

    for k, M, gen, expected, name in test_programme:
  
        LHS = sorted(gen(k=k, M=M))
        RHS = sorted(expected)

        print("Test '",name,"' has LHS and RHS:")
        for i,j in zip(LHS,RHS):
            print(i, j)
        print()

        assert LHS==RHS

