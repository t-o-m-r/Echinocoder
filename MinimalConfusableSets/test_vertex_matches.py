
import vertex_matches

# Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.
# "Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).



k4M4_all_canonical_matches_expected = [
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

    k4M4_all_canonical_matches_computed = list(vertex_matches.generate_all_canonical_matches(
        k=2, # k=dimension of space
        M=4, #number of bad bats
        ))

    LHS = sorted(k4M4_all_canonical_matches_computed)
    RHS = sorted(k4M4_all_canonical_matches_expected)

    print("k4M4_all_canonical_matches LHS and RHS were")
    for i,j in zip(LHS,RHS):
        print(i, j)
    print()

    assert LHS==RHS

