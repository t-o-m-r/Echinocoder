#import itertools
import math
from vertex_matches import (
    generate_all_vertex_match_signatures,
    generate_all_vertex_matches,
    _smallest_odd_number_greater_than_or_equal_to,
)

from distinct_permutations_with_leftovers import distinct_permutations_with_leftovers as distinct_permutations
from distinct_partitions_with_start import distinct_partitions_with_start as distinct_partitions
from bi_range import bi_range_with_maxes
from equivalent_places import Equivalent_Places

def _old_generate_all_vertex_match_signatures(
    M, #number of bad bats
    k = None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
    start = None
    ):
    """
    The signature of a vertex match is how many ones, minus ones and zeros it has.
    We yield triplets of numbers having the order (number_ones, number_minus_ones, number_zeros).

    If suplied and not None, start must be a tuple containing a signature which the method would ordinarily generate, and as a consequence the generator will start here.

    Vertex matches have M entries in total, comprising an even number of +1 and and odd number of -1 entries, and others zero.

    "Useful" vertex matches have at least k+1 non-zero entries (because all sums of <=k linearly dependent non-zero things in k-dimes are non-zero).
    """

    if start is not None:
        starting = True
        if len(start) != 3:
            raise ValueError(f"len(start) should equal 3 but is {len(start)}. start={start}.")
        if sum(start) != M:
            raise ValueError(f"sum(start) should equal {M} but is {sum(start)}. start={start}.")
        if True in ((int(c) != c or c<0) for c in start):
            raise ValueError(f"start should be a tuple of non-negative integers but start={start}.")

        start_ones, start_minus_ones, _ = start
    else:
        starting = False

    for number_of_ones in range(start_ones if starting else 0, M+1, 2):

        if starting:
            start_for_number_of_minus_ones = start_minus_ones
        else:
            if k is not None:
                # In this case we need
                #         number_of_ones + number_of_minus_ones > k  and   number_of_minus_ones >= 1
                # so
                #         number_of_minus_ones > k - number_of_ones   and number_of_minus_ones >= 1
                # so
                #         number_of_minus_ones >= k - number_of_ones + 1 and number_of_minus_ones >=1
                # so
                #         number_of_minus_ones >= max(k - number_of_ones + 1, 1)
                start_for_number_of_minus_ones =  max(1, _smallest_odd_number_greater_than_or_equal_to(k - number_of_ones + 1))
            else:
                start_for_number_of_minus_ones = 1

        for number_of_minus_ones in range(start_for_number_of_minus_ones, M+1-number_of_ones, 2):
            # In an alternative (but slower) implementation, one could always have start_for_number_of_minus_ones=1 but then
            # uncomment the next two lines:
            # if k is not None and (number_of_ones + number_of_minus_ones <= k):
            #      continue
            number_of_zeros = M-number_of_ones-number_of_minus_ones
            if starting:
                assert (number_of_ones, number_of_minus_ones, number_of_zeros) == start
                starting = False
            yield number_of_ones, number_of_minus_ones, number_of_zeros
    assert starting == False


def generate_all_useful_vertex_matches(
    M, # M=number of bad bats
    k, # k=dimension of space 
    permute = True,
    ):
    yield from generate_all_vertex_matches(M=M, k=k, permute=permute)


def generate_all_useful_vertex_matches_given_perming_places(
        M, # M=number of bad bats
        k, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        perming_places = 0, # permutations take place within the first "perming_places" places, otherwise not.
        ):
    yield from generate_all_vertex_matches_given_perming_places(M, k=k, perming_places=perming_places)

def generate_all_vertex_matches_given_perming_places(
        M, # M=number of bad bats
        k=None, # k=dimension of space (supply k if you want to calculate only useful matches, otherwise omit)
        perming_places = 0, # permutations take place within the first "perming_places" places, otherwise not.
        ):

        if M<0:
            raise ValueError(f"M should be a non-negative integer but is {M}.")

        if perming_places<0 or perming_places>M:
            raise ValueError(f"perming_places should be in [0,{M}]  but is {perming_places}.")

        non_perming_places = M-perming_places

        for number_of_ones, number_of_minus_ones, number_of_zeros in generate_all_vertex_match_signatures(M,k=k):

            for perming_ones, non_perming_ones in bi_range_with_maxes(number_of_ones, max_first=perming_places, max_second=non_perming_places):
                for perming_minus_ones, non_perming_minus_ones in bi_range_with_maxes(number_of_minus_ones, max_first = perming_places-perming_ones, max_second=non_perming_places - non_perming_ones):
                    perming_zeros = perming_places - (perming_ones + perming_minus_ones)
                    non_perming_zeros = number_of_zeros - perming_zeros

                    assert perming_zeros >=0
                    assert non_perming_zeros >=0

                    perming_part = (-1,)*perming_minus_ones + (0,)*perming_zeros + (1,)*perming_ones # Note numerical order!
                    non_perming_part = (-1,)*non_perming_minus_ones + (0,)*non_perming_zeros + (1,)*non_perming_ones # Note numerical order!

                    for perm in distinct_permutations(perming_part):
                        yield perm + non_perming_part


                  
def demo():
    M=4
    for perming_places in range(5):
        print(f"All matches, given M={M} bad bats, for perming_places={perming_places}")
        for i,match in enumerate(generate_all_vertex_matches_given_perming_places(M=M, perming_places=perming_places)):
           print(f"   {i+1}:    {match}")
        print()
    k=2
    for perming_places in range(5):
        print(f"All USEFUL matches in k={k} dimensions, given M={M} bad bats, for perming_places={perming_places}")
        for i,match in enumerate(generate_all_useful_vertex_matches_given_perming_places(k=k, M=M, perming_places=perming_places)):
           print(f"   {i+1}:    {match}")
        print()

if __name__ == "__main__":
    demo()

