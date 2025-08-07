#import itertools
from distinct_permutations import distinct_permutations

# Canonical matches have an even number of +1 and and odd number of -1 entries, and others zero.
# "Useful" canonical matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).

def generate_all_useful_canonical_matches(
        k, # k=dimension of space
        M, #number of bad bats
        ):

        for match in generate_all_canonical_matches(k=k, M=M, show_only_useful_matches = True):
            yield match


def generate_all_canonical_matches(
        k, # k=dimension of space
        M, #number of bad bats
        show_only_useful_matches = False,
        ):

        for number_of_ones in range(0, M+1, 2):
            ones = (1,)*number_of_ones
            for number_of_minus_ones in range(1, M+1-number_of_ones, 2):
                if show_only_useful_matches and (number_of_ones + number_of_minus_ones <= k):
                    continue
                minus_ones = (-1,)*number_of_minus_ones
                number_of_zeroes= M-number_of_ones-number_of_minus_ones
                zeros = (0,)*number_of_zeroes

                for match in distinct_permutations( ones + minus_ones + zeros):
                    yield match

