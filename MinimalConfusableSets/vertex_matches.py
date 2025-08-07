#import itertools
import math
from distinct_permutations import distinct_permutations

# Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.

# "Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).

def smallest_odd_number_greater_than_or_equal_to(x):
  return 2*math.ceil((x+1)/2)-1 

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
                number_of_zeroes= M-number_of_ones-number_of_minus_ones
                zeros = (0,)*number_of_zeroes

                if permute:
                    for match in distinct_permutations( ones + minus_ones + zeros):
                        yield match
                else:
                    yield ones + minus_ones + zeros


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
