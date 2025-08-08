#import itertools
import math
from distinct_permutations import distinct_permutations

"""
Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.

"Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).

Sometimes it is not worth permuting canonical matches over every bad bad because other matches in the existing context may not yet have broken any symmetries between the bats.  WLOG we choose to put the entries which are deemed to have already broen symmetry FIRST.  And the argument "fixed_places" describes how many such spaces there are.
E.g.: fixed_places=2 means that the first two position (i.e. pos 0 and pos 1) have broken some symmetry and permutations on them are relevant, whereas permutations on pos 2 and above are irrelevant.
E.g. if one listed all distinct permutations of the letters "Speedo" for "fixed_places=2" one would want these (in which the "." is not actually part of the string but has been inserted to help guide the eye so that you can see that only the first two letters explore all perms wile after the dot there is no perming.  Note that there are 4*4+5 = 21 of these:

    Sp.eedo
    Se.pedo
    Sd.peeo
    So.peed

    pS.eedo
    pe.Sedo
    pd.Seeo
    po.Seed

    eS.pedo
    ep.pedo
    ee.pedo  # Yes, this group has five on account of the double "e" !
    ed.pedo
    eo.Sped

    dS.peeo
    dp.Seep
    de.Speo
    do.Spee

    oS.peed
    op.Seed
    oe.Sped
    od.Spee
"""


def smallest_odd_number_greater_than_or_equal_to(x):
  return 2*math.ceil((x+1)/2)-1 

def bi_range(n):
    """
    Whereas range(n) iterates over 0,1,2,3,...,n-1 ... bi_range(n) iterates over non-negative pairs of integers which sum to n.
    The first integer grows, while the second integer shrinks.
    For example, range(4) would iterate over
        (0,4), (1,3), (2,2), (3,1), (4,0).
    """
    for i in range(n+1):
        yield i, n-i

def bi_range_with_maxes_crude(n, max_first, max_second):
    """
    Whereas range(n) iterates over 0,1,2,3,...,n-1 ... bi_range(n) iterates over non-negative pairs of integers which sum to n.
    The first integer grows, while the second integer shrinks.
    The first integer may not exceed max_first, while the second may not exceed max_second.
    For example, range(4, 2,3) would iterate over
         (1,3), (2,2)
    which starts at the max_second contraint, and goes to the max_first constraint.
    If the sum of both maxes is less than the total n, there will be no valid iterator positions. So:
    """
   
    for i in range(n+1):
       if i>max_first or n-i>max_second:
           continue # TODO! Slow Fix!
       yield i, n-i

def bi_range_with_maxes(n, max_first, max_second):
    """
    Whereas range(n) iterates over 0,1,2,3,...,n-1 ... bi_range(n) iterates over non-negative pairs of integers which sum to n.
    The first integer grows, while the second integer shrinks.
    The first integer may not exceed max_first, while the second may not exceed max_second.
    For example, range(5, 2,3) would iterate over
         (1,3), (2,2)
    which starts at the max_second contraint, and goes to the max_first constraint.
    If the sum of both maxes is less than the total n, there will be no valid iterator positions. So:

    0 <= a <= A
    0 <= b <= B
    0 <= a+b = N

    so 

    0 <= a <= A
    0 <= N-a <= B

    so

    0 <= a <= A
    0 >= a-N >= -B

    so

    0 <= a <= A
    N >= a >= N-B

    so

    0 <= a <= A
    N-B <= a <= N

    so

    max(0, N-B) <= a <= min(A,N)

    """
  
    if n<0 or max_first<0 or max_second<0:
        # No valid iterator positions can be returned.
        return
    
    for a in range(max(0, n-max_second), min(max_first, n)+1):
        yield a, n-a


def generate_all_useful_canonical_matches(
        k, # k=dimension of space
        M, #number of bad bats
        permute = True,
        ):
        yield from generate_all_canonical_matches(k=k, M=M, show_only_useful_matches = True, permute=permute)


def generate_all_canonical_matches(
        k, # k=dimension of space
        M, #number of bad bats
        show_only_useful_matches = False,
        permute = True,
        ):

        for number_of_ones in range(0, M+1, 2):
            ones = (1,)*number_of_ones

            if show_only_useful_matches:
                # In this case we need 
                #         number_of_ones + number_of_minus_ones > k  and   number_of_minus_ones >= 1
                # so
                #         number_of_minus_ones > k - number_of_ones   and number_of_minus_ones >= 1
                # so
                #         number_of_minus_ones >= k - number_of_ones + 1 and number_of_minus_ones >=1
                # so
                #         number_of_minus_ones >= max(k - number_of_ones + 1, 1)
                start_for_number_of_minus_ones =  max(1, smallest_odd_number_greater_than_or_equal_to(k - number_of_ones + 1))
            else:
                start_for_number_of_minus_ones = 1
            for number_of_minus_ones in range(start_for_number_of_minus_ones, M+1-number_of_ones, 2):
                # In alternative (but slower) implementation, one could always have start_for_number_of_minus_ones=1 but then 
                # uncomment the next two lines:
                # if show_only_useful_matches and (number_of_ones + number_of_minus_ones <= k):
                #      continue
                minus_ones = (-1,)*number_of_minus_ones
                number_of_zeros= M-number_of_ones-number_of_minus_ones
                zeros = (0,)*number_of_zeros

                if permute:
                    for match in distinct_permutations( ones + minus_ones + zeros):
                        yield match
                else:
                    yield ones + minus_ones + zeros

def generate_all_useful_matches_given_fixed_places(
        k, # k=dimension of space
        M, # number of bad bats
        fixed_places = 0, # permutations take place within the first "fixed_places" places, otherwise not.
        ):
    yield from generate_all_matches_given_fixed_places(k=k, M=M, show_only_useful_matches = True, fixed_places=fixed_places)
    
def generate_all_matches_given_fixed_places(
        k, # k=dimension of space
        M, # number of bad bats
        show_only_useful_matches = False,
        fixed_places = 0, # permutations take place within the first "fixed_places" places, otherwise not.
        ):

        if M<0:
            raise ValueError(f"M should be a non-negative integer but is {M}.")

        if fixed_places<0 or fixed_places>M:
            raise ValueError(f"fixed_places should be in [0,{M}]  but is {fixed_places}.")

        non_fixed_places = M-fixed_places

        for number_of_ones in range(0, M+1, 2):
            #ones = (1,)*number_of_ones

            if show_only_useful_matches:
                # In this case we need 
                #         number_of_ones + number_of_minus_ones > k  and   number_of_minus_ones >= 1
                # so
                #         number_of_minus_ones > k - number_of_ones   and number_of_minus_ones >= 1
                # so
                #         number_of_minus_ones >= k - number_of_ones + 1 and number_of_minus_ones >=1
                # so
                #         number_of_minus_ones >= max(k - number_of_ones + 1, 1)
                start_for_number_of_minus_ones =  max(1, smallest_odd_number_greater_than_or_equal_to(k - number_of_ones + 1))
            else:
                start_for_number_of_minus_ones = 1
            for number_of_minus_ones in range(start_for_number_of_minus_ones, M+1-number_of_ones, 2):
                # In alternative (but slower) implementation, one could always have start_for_number_of_minus_ones=1 but then 
                # uncomment the next two lines:
                # if show_only_useful_matches and (number_of_ones + number_of_minus_ones <= k):
                #      continue
                #minus_ones = (-1,)*number_of_minus_ones
                number_of_zeros= M-number_of_ones-number_of_minus_ones
                #zeros = (0,)*number_of_zeros

                for perming_ones, non_perming_ones in bi_range_with_maxes(number_of_ones, max_first=fixed_places, max_second=non_fixed_places):
                    for perming_minus_ones, non_perming_minus_ones in bi_range_with_maxes(number_of_minus_ones, max_first = fixed_places-perming_ones, max_second=non_fixed_places - non_perming_ones):
                        perming_zeros = fixed_places - (perming_ones + perming_minus_ones)
                        non_perming_zeros = number_of_zeros - perming_zeros

                        assert perming_zeros >=0
                        assert non_perming_zeros >=0

                        perming_part = (1,)*perming_ones + (-1,)*perming_minus_ones + (0,)*perming_zeros
                        non_perming_part = (1,)*non_perming_ones + (-1,)*non_perming_minus_ones + (0,)*non_perming_zeros

                        for perm in distinct_permutations(perming_part):
                            yield perm + non_perming_part


if __name__ == "__main__":
    M=4
    print(f"All matches given M={M} bad bats are:")
    for i, match in enumerate(generate_all_canonical_matches(k=None, M=M)):
       print(f"   {i+1}:    {match}")
    print()

    k=2
    print(f"All USEFUL matches in k={k} dimensions, given M={M} bad bats are:")
    for i,match in enumerate(generate_all_useful_canonical_matches(k=k, M=M)):
       print(f"   {i+1}:    {match}")
    print()

    print(f"All matches in k={k} dimensions, given M={M} bad bats, but ignoring permutations are:")
    for i,match in enumerate(generate_all_canonical_matches(k=k, M=M, permute=False)):
       print(f"   {i+1}:    {match}")
    print()

    print(f"All USEFUL matches in k={k} dimensions, given M={M} bad bats, but ignoring permutations are:")
    for i,match in enumerate(generate_all_useful_canonical_matches(k=k, M=M, permute=False)):
       print(f"   {i+1}:    {match}")
    print()

    for fixed_places in range(5):
        print(f"All matches in k={k} dimensions, given M={M} bad bats, for fixed_places={fixed_places}")
        for i,match in enumerate(generate_all_matches_given_fixed_places(k=k, M=M, fixed_places=fixed_places)):
           print(f"   {i+1}:    {match}")
        print()

    for fixed_places in range(5):
        print(f"All USEFUL matches in k={k} dimensions, given M={M} bad bats, for fixed_places={fixed_places}")
        for i,match in enumerate(generate_all_useful_matches_given_fixed_places(k=k, M=M, fixed_places=fixed_places)):
           print(f"   {i+1}:    {match}")
        print()
